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

# Define project specific needs directives

needs_types = [
    # Requirements
    dict(
        directive="stkh_req",
        title="Stakeholder requirements",
        prefix="STKH_REQ__",
        color="#BFD8D2",
        style="node",
    ),
    dict(
        directive="tool_req",
        title="Tool Requirements",
        prefix="TOOL_REQ__",
        color="#BFD8D2",
        style="node",
    ),
]

# Define extra options for needs object
needs_extra_options = [
    "security",
    "safety",
    "level",
    "rationale",
    "mitigated_by",
    "reqtype",
    "codelink",
    "testlink",
    "reqcovered",
    "testcovered",
]

needs_extra_links = [
    # TODO: Refer process document for the usage of links
    {
        "option": "satisfies",
        "incoming": "is satisfied by",
        "outgoing": "satisfies",
        "style_start": "-up",
        "style_end": "->",
    },
    {"option": "implements", "incoming": "implements by", "outgoing": "implements"},
]
