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

load("//docs:_tooling/docs.bzl", "all_docs_targets")
load("//docs:_tooling/extensions/score_source_code_linker/collect_source_files.bzl", "parse_source_files_for_needs_links")

parse_source_files_for_needs_links(
    name="all_module_source_files",
    # no source files added for now
)

# Creates all documentation targets:
# - `docs:incremental` for building docs incrementally at runtime
# - `docs:live_preview` for live preview in the browser without an IDE
# - `docs:ide_support` for creating python virtualenv for IDE support
# - `docs:docs` for building documentation at build-time
# - `docs:plantuml` and `:plantuml_for_python` targets, to be used as dependencies for plantuml generation
all_docs_targets(source_code_linker="//docs2:all_module_source_files")
