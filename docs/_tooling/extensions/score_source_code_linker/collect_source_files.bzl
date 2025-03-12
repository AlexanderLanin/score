# *******************************************************************************
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
# SPDX-License-Identifier: Apache-2.0
# *******************************************************************************
"""Defines Bazel targets for linking source code to documentation."""

load("@aspect_rules_py//py:defs.bzl", "py_binary")

CollectedFilesInfo = provider(
    doc = "All collected source files via aspect.",
    fields = {
        "files": "depset of source files",
    },
)

SourceCodeLinks = provider(
    doc = "All source code links found in the source files.",
    fields = {
        "file": "Path to json file containing the source code links.",
    },
)

def _extract_source_files(rule, attr):
    collected_source_files = []
    if hasattr(rule.attr, attr):
        for src in getattr(rule.attr, attr):
            for f in src.files.to_list():
                if not f.path.startswith("external"):
                    collected_source_files.append(f)
    return collected_source_files

def _get_all_source_files(rule):
    # type: (Unknown) -> List[File]
    """
    Collects all source files for a rule.

    Assumption: srcs and hdrs are the only attributes that contain source files
    """
    collected_source_files = []
    collected_source_files += _extract_source_files(rule, "srcs")
    collected_source_files += _extract_source_files(rule, "hdrs")
    return collected_source_files

def _collect_source_files_aspect_impl(_target, ctx):
    # type: (Target, Unknown) -> List[CollectedFilesInfo]

    # This function is called for every deps entry in the build tree.
    # Source files of the current target are collected into source_files.
    # Source files of dependencies are collected into source_files_of_dependencies.

    source_files = _get_all_source_files(ctx.rule)
    if hasattr(ctx.rule.attr, "deps"):
        # Collect source files of dependencies via the .files attribute which is returned in this
        # function.
        source_files_of_dependencies = [dep[CollectedFilesInfo].files for dep in ctx.rule.attr.deps]
    else:
        # If there are no dependencies, the source_files_of_dependencies is an empty list.
        source_files_of_dependencies = []

    # depset merges the source files of the current target and its dependencies into one list.
    return [CollectedFilesInfo(files = depset(source_files, transitive = source_files_of_dependencies))]

# Define an aspect that collects all source files from a target and its dependencies.
# Hint: Aspect is the bazel version of a visitor pattern. Those tend to be better known,
# and/or easier to understand.
collect_source_files_aspect = aspect(
    # Calls the _collect_source_files_aspect_impl function for every target that is reachable
    # from the target that the aspect is applied to by following the deps attribute.
    implementation = _collect_source_files_aspect_impl,
    attr_aspects = ["deps"],
)

def _collect_and_parse_source_files_impl(ctx):
    sources_filename = ctx.label.name
    srcs_filelist_file = ctx.actions.declare_file("%s_sources.txt" % sources_filename)

    # Collect files from each dependency (.files contains direct and transitive dependencies)
    accumulated = []
    for dep in ctx.attr.deps:
        accumulated.append(dep[CollectedFilesInfo].files)

    # Flatten the list of files
    all_files = depset(transitive = accumulated).to_list()

    content = ""
    for filename in all_files:
        content += "%s\n" % filename.path

    ctx.actions.write(srcs_filelist_file, content)

    parsed_sources_json_file = ctx.actions.declare_file("%s.json" % ctx.label.name)

    args = ctx.actions.args()
    args.add(srcs_filelist_file)
    args.add("--output", parsed_sources_json_file)

    ctx.actions.run(
        arguments = [args],
        executable = ctx.executable._source_files_parser,
        inputs = [srcs_filelist_file] + all_files,
        outputs = [parsed_sources_json_file],
    )

    return [
        DefaultInfo(
            files = depset([parsed_sources_json_file]),
            runfiles = ctx.runfiles([parsed_sources_json_file]),
        ),
        SourceCodeLinks(file = parsed_sources_json_file),
    ]

_collect_and_parse_source_files = rule(
    implementation = _collect_and_parse_source_files_impl,
    attrs = {
        "deps": attr.label_list(
            aspects = [collect_source_files_aspect],
            allow_files = True,
            doc = "Dependencies and files to scan for links to needs-elements (e.g. requirements).",
        ),
        "_source_files_parser": attr.label(
            default = ":_source_files_parser",
            executable = True,
            cfg = "exec",
        ),
    },
)

def parse_source_files_for_needs_links(
        srcs,
        name = "collected_files_for_score_source_code_linker"):
    """
    Collects and parses source files for linking source code to documentation.

    Returns Label for the bazel rule.
    """

    # Binary which based a list of source files, parses them for links to needs-elements,
    # and writes the result to a file.
    # Used by _collect_and_parse_source_files() rule.
    py_binary(
        name = "_source_files_parser",
        srcs = ["//docs:_tooling/extensions/score_source_code_linker/parse_source_files.py"],
        # visibility = ["//visibility:public"],
    )

    # Rule which collects source files (at build time) and calls the binary to parse them (at runtime)???
    _collect_and_parse_source_files(
        name = name,
        deps = srcs,  # how do we name this? # TODO
    )

    pkg = native.package_name()
    return Label("@//" + pkg + ":" + name)
