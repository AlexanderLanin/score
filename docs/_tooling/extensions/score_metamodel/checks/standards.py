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
from sphinx_needs.data import NeedsInfoType

from docs._tooling.extensions.score_metamodel import graph_check, CheckLogger, NeedsInfoType


def get_standard_prefixes() -> list:
    """
    Return a list of standard prefixes.
    """
    return ["R_ISO2143", "R_ISO26262", "R_ISOPAS8926"]


def get_standards_needs(needs) -> dict:
    """
    Return a dictionary of all standard requirements from the Sphinx app's needs.
    """
    standards_prefixes = get_standard_prefixes()

    return {
        need["id"]: need
        for need in needs.values()
        if need["id"].startswith(tuple(standards_prefixes)) and "RQ" in need["id"]
    }


def get_standards_workproducts(needs) -> dict:
    """
    Return a dictionary of standard workproducts from the Sphinx app's needs.
    """
    standards_prefixes = get_standard_prefixes()

    return {
        need["id"]: need
        for need in needs.values()
        if need["id"].startswith(tuple(standards_prefixes)) and "WP" in need["id"]
    }


def get_workflows(needs) -> dict:
    """
    Return a dictionary of all workflows from the Sphinx app's needs.
    """

    return {
        need["id"]: need for need in needs.values() if need.get("type") == "workflow"
    }


def get_workproducts(needs) -> dict:
    """
    Return a dictionary of all workproducts from the Sphinx app's needs.
    """

    return {
        need["id"]: need for need in needs.values() if need.get("type") == "workproduct"
    }


def get_compliance_gd_needs(needs) -> set:
    """
    Return a set of all compliance_gd values from the Sphinx app's needs.
    """
    return {
        complience_gd
        for need in needs.values()
        for complience_gd in need.get("compliance-gd", [])
        if complience_gd
    }


def get_compliance_wp_needs(needs) -> set:
    """
    Return a set of all compliance_wp values from the Sphinx app's needs.
    """

    return {
        complience_wp
        for need in needs.values()
        for complience_wp in need.get("compliance-wp", [])
        if complience_wp
    }


@graph_check
def check_all_standard_req_linked_item_via_the_compliance_gd(
    needs: list[dict], log: CheckLogger
) -> bool:
    """
    Checks if all standard requirements are linked to an item via the compliance_gd tag.
    Logs a warning for each unlinked standard requirement.
    Returns True if any standard requirement is unlinked, otherwise False.
    """
    standards_needs = get_standards_needs(needs)
    compliance_gd_needs = get_compliance_gd_needs(needs)

    for need in standards_needs.values():
        if need["id"] not in compliance_gd_needs:
            msg = f"Standard requirement `{need['id']}` is not linked to at least one item via the compliance-gd tag. \n"
            log.warning_for_option(need, "id", msg)


@graph_check
def check_all_standard_workproducts_linked_item_via_the_compliance_wp(
    needs: list[dict], log: CheckLogger
) -> bool:
    """
    Checks if all standard work products are linked to an item via the compliance_wp tag.
    Logs a warning for each unlinked standard work product.
    Returns True if any standard work product is unlinked, otherwise False.
    """
    standards_workproducts = get_standards_workproducts(needs)
    compliance_wp_needs = get_compliance_wp_needs(needs)

    for need in standards_workproducts.values():
        if need["id"] not in compliance_wp_needs:
            msg = (
                f"Standard workproduct `{need['id']}` is not linked to at least one item "
                f"via the compliance-wp tag. \n"
            )
            log.warning_for_option(need, "id", msg)


@graph_check
def check_workproduct_uniqueness_over_workflows(needs: list[dict], log: CheckLogger) -> bool:
    """
    Check if all workproducts are contained in exactly one workflow.
    Logs workflow IDs when a workproduct is contained in multiple workflows.
    """
    all_workflows = get_workflows(needs)
    all_workproducts = get_workproducts(needs)

    # Map to track counts for each workproduct and their associated workflows
    workproduct_analysis = {
        wp["id"]: {"count": 0, "workproduct": wp, "workflows": []}
        for wp in all_workproducts.values()
    }

    # Iterate over workflows and update the counts and workflows
    for workflow_id, workflow in all_workflows.items():
        for output in workflow["output"]:
            # If the workproduct is in the analysis, increment its count and add the workflow_id
            if output in workproduct_analysis:
                workproduct_analysis[output]["count"] += 1
                workproduct_analysis[output]["workflows"].append(workflow_id)

    # Check for mismatches and log error
    for analysis in workproduct_analysis.values():
        count = analysis["count"]
        workproduct = analysis["workproduct"]
        workflows = analysis["workflows"]

        if count != 1:  # Mismatch found
            if count == 0:
                msg = f"Workproduct `{workproduct['id']}` is not contained in any workflow, which is incorrect. \n"
                log.warning_for_need(workproduct, msg)
            else:
                workflows_str = ", ".join(
                    f"`{workflow}`" for workflow in workflows
                )  # Join workflow IDs into a string
                msg = f"Workproduct `{workproduct['id']}` is contained in {count} workflows: {workflows_str}, which is incorrect. \n"
                log.warning_for_need(workproduct, msg)


def my_pie_linked_standard_requirements(needs, results, **kwargs):
    """
    Function to render the chart of check for standard requirements linked to at least an item via complience-gd.
    """
    cnt_connected = 0
    cnt_not_connected = 0

    standards_needs = get_standards_needs(needs)
    compliance_gd_needs = get_compliance_gd_needs(needs)

    for need in standards_needs.values():
        if need["id"] in compliance_gd_needs:
            cnt_connected += 1
        else:
            cnt_not_connected += 1

    results.append(cnt_connected)
    results.append(cnt_not_connected)


def my_pie_linked_standard_workproducts(needs, results, **kwargs):
    """
    Function to render the chart of check for standar workproducts linked to at least an item via complience-wp.
    """
    cwp_connected = 0
    cwp_not_connected = 0

    standard_workproducts = get_standards_workproducts(needs)

    compliance_wp_needs = get_compliance_wp_needs(needs)

    for need in standard_workproducts.values():
        if need["id"] in compliance_wp_needs:
            cwp_connected += 1
        else:
            cwp_not_connected += 1

    results.append(cwp_connected)
    results.append(cwp_not_connected)


def my_pie_workproducts_contained_in_exactly_one_workflow(needs, results, **kwargs):
    """
    Function to render the chart of check for workproducts that are contained in exactly one workflow, the not connected once and the once that are connected to multiple workflows.
    """
    all_workflows = get_workflows(needs)
    all_workproducts = get_workproducts(needs)

    # Map to track counts for each workproduct and their associated workflows
    workproduct_analysis = {wp["id"]: {"count": 0} for wp in all_workproducts.values()}

    # Iterate over workflows and update the counts and workflows
    for workflow_id, workflow in all_workflows.items():
        for output in workflow["output"]:
            # If the workproduct is in the analysis, increment its count and add the workflow_id
            if output in workproduct_analysis:
                workproduct_analysis[output]["count"] += 1

    nb_wp_connected_to_one_workflow = nb_wp_connected_to_more_than_one_workflow = (
        not_connected_wp
    ) = 0

    for analysis in workproduct_analysis.values():
        count = analysis["count"]

        if count == 0:
            not_connected_wp += 1
        elif count == 1:
            nb_wp_connected_to_one_workflow += 1
        else:
            nb_wp_connected_to_more_than_one_workflow += 1

    results.append(not_connected_wp)
    results.append(nb_wp_connected_to_one_workflow)
    results.append(nb_wp_connected_to_more_than_one_workflow)
