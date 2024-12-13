# *******************************************************************************
# Copyright (c) 2024 Contributors to the Eclipse Foundation
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

load("@aspect_rules_py//py:defs.bzl", "py_venv")
load("@pip_sphinx//:requirements.bzl", "all_requirements", "requirement")
load("@rules_pkg//pkg:mappings.bzl", "pkg_files")
load("@rules_pkg//pkg:tar.bzl", "pkg_tar")
load("@rules_python//python:defs.bzl", "py_library")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")
load("@rules_python//sphinxdocs:sphinx.bzl", "sphinx_build_binary", "sphinx_docs")

# all_requirements include esbonio which we don't need most of the time.
# Hint: the names are e.g. "@@rules_python~~pip~pip_sphinx//esbonio:pkg"
sphinx_requirements = [name for name in all_requirements if not "esbonio" in name] + [":extensions"]

sphinx_docs(
    name = "docs",
    srcs = glob([
        "**/*.png",
        "**/*.svg",
        "**/*.rst",
        "**/*.html",
        "**/*.css",
    ]),
    config = ":conf.py",
    extra_opts = [
        "-W",
        "--keep-going",
    ],
    formats = [
        "html",
    ],
    sphinx = ":sphinx_build",
    tags = [
        "manual",
    ],
)

sphinx_build_binary(
    name = "sphinx_build",
    deps = sphinx_requirements,
)

py_library(
    name = "extensions",
    srcs = [
        "_extensions/layouts.py",
        "_extensions/metamodel.py",
    ],
    imports = ["."],
)

compile_pip_requirements(
    name = "requirements",
    src = "requirements.txt",
    requirements_txt = "requirements_lock.txt",
    tags = [
        "manual",
    ],
)

filegroup(
    name = "html",
    srcs = [":docs"],
    output_group = "html",
)

pkg_files(
    name = "html_files",
    srcs = [":html"],
    renames = {"html": ""},
)

pkg_tar(
    name = "github-pages",
    srcs = [":html_files"],
)

# Run-time build of documentation, incl. incremental build support.
py_binary(
    name = "incremental",
    srcs = ["incremental.py"],
    deps = sphinx_requirements,
)

# Virtual python environment for working on the documentation (esbonio).
# incl. python support when working on conf.py and sphinx extensions.
py_venv(
    name = "ide_support",
    venv_name = ".venv_docs",
    # Until release of esbonio 1.x, we need to install it ourselves so the VS Code extension can find it.
    deps = sphinx_requirements + [requirement("esbonio")],
)
