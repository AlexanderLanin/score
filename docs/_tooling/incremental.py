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

import argparse
import os
import subprocess

import debugpy
from sphinx.cmd.build import main as sphinx_main

parser = argparse.ArgumentParser()
parser.add_argument(
    "-dp", "--debug_port", help="port to listen to debugging client", default=5678
)
parser.add_argument("--debug", help="Enable Debugging via debugpy", action="store_true")
args = parser.parse_args()
if args.debug:
    debugpy.listen(("0.0.0.0", args.debug_port))
    print("Waiting for client to connect on port: " + str(args.debug_port))
    debugpy.wait_for_client()
    pass

# sphinx will print relative paths to the current directory.
# Change to the workspace root so that the paths are readable and clickable.
workspace = os.getenv("BUILD_WORKSPACE_DIRECTORY")

# Initialize with a default value
source_code_linker_file = ""


def get_env(name):
    val = os.environ.get(name, None)
    print(f"Env: {name} = {val}")
    if val is None:
        raise ValueError(f"Environment variable {name} is not set")
    return val


if workspace:
    # This will gives us all 'output files' and their location that are required
    #  by the 'source_link' extensions
    # Build and run SOURCE_CODE_LINKER (it's run at build time)
    subprocess.run(
        [
            "bazel",
            "build",
            "--noremote_accept_cached",
            get_env("SOURCE_CODE_LINKER"),
        ],
        cwd=workspace,
    )

    # Query where the output files are
    process = subprocess.Popen(
        [
            "bazel",
            "cquery",
            get_env("SOURCE_CODE_LINKER"),
            "--output=files",
        ],
        cwd=workspace,
        stdout=subprocess.PIPE,
    )

    source_code_linker_file = (
        process.stdout.readline().decode().strip() if process.stdout else ""
    )

    os.chdir(workspace)

sphinx_main(
    [
        get_env("SOURCE_DIRECTORY"),
        get_env("BUILD_DIRECTORY"),
        "-W",  # treat warning as errors
        "--keep-going",  # do not abort after one error
        "-T",  # show details in case of errors in extensions
        "--jobs",
        "auto",
        "--conf-dir",
        get_env("CONF_DIRECTORY"),
        f"--define=source_code_linker_file={source_code_linker_file}",
    ]
)
