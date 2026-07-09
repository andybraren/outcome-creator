"""Jira API utilities for the outcome-creator pipeline."""

import json
import os
import re
import subprocess
import sys
from typing import Any

import requests


def get_jira_config() -> dict[str, str]:
    """Get Jira connection configuration from environment variables."""
    server = os.environ.get("JIRA_SERVER", "")
    user = os.environ.get("JIRA_USER", "")
    token = os.environ.get("JIRA_TOKEN", "")

    if not all([server, user, token]):
        missing = []
        if not server:
            missing.append("JIRA_SERVER")
        if not user:
            missing.append("JIRA_USER")
        if not token:
            missing.append("JIRA_TOKEN")
        print(f"Warning: Missing environment variables: {', '.join(missing)}", file=sys.stderr)

    return {"server": server.rstrip("/"), "user": user, "token": token}


def jira_request(method: str, path: str, data: dict | None = None) -> dict[str, Any]:
    """Make an authenticated Jira REST API request."""
    config = get_jira_config()
    url = f"{config['server']}/rest/api/3/{path.lstrip('/')}"

    response = requests.request(
        method,
        url,
        auth=(config["user"], config["token"]),
        json=data,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json() if response.text else {}


def fetch_issue(key: str) -> dict[str, Any]:
    """Fetch a single Jira issue by key."""
    return jira_request("GET", f"issue/{key}")


def search_issues(jql: str, max_results: int = 50) -> list[dict[str, Any]]:
    """Search for issues using JQL."""
    data = {"jql": jql, "maxResults": max_results, "fields": ["summary", "description", "status", "priority",
                                                                "issuetype", "components", "labels", "assignee",
                                                                "reporter", "created", "updated"]}
    result = jira_request("POST", "search", data)
    return result.get("issues", [])


def create_issue(project: str, issue_type: str, summary: str, description: str,
                 priority: str = "Major", components: list[str] | None = None,
                 labels: list[str] | None = None) -> dict[str, Any]:
    """Create a new Jira issue."""
    fields: dict[str, Any] = {
        "project": {"key": project},
        "issuetype": {"name": issue_type},
        "summary": summary,
        "description": _text_to_adf(description),
        "priority": {"name": priority},
    }

    if components:
        fields["components"] = [{"name": c} for c in components]
    if labels:
        fields["labels"] = labels

    return jira_request("POST", "issue", {"fields": fields})


def update_issue(key: str, fields: dict[str, Any]) -> dict[str, Any]:
    """Update an existing Jira issue."""
    if "description" in fields and isinstance(fields["description"], str):
        fields["description"] = _text_to_adf(fields["description"])
    return jira_request("PUT", f"issue/{key}", {"fields": fields})


def add_labels(key: str, labels: list[str]) -> None:
    """Add labels to a Jira issue."""
    update = {"labels": [{"add": label} for label in labels]}
    jira_request("PUT", f"issue/{key}", {"update": update})


def remove_labels(key: str, labels: list[str]) -> None:
    """Remove labels from a Jira issue."""
    update = {"labels": [{"remove": label} for label in labels]}
    jira_request("PUT", f"issue/{key}", {"update": update})


def add_comment(key: str, body: str) -> dict[str, Any]:
    """Add a comment to a Jira issue."""
    return jira_request("POST", f"issue/{key}/comment", {"body": _text_to_adf(body)})


def create_link(from_key: str, to_key: str, link_type: str = "is part of") -> dict[str, Any]:
    """Create a link between two Jira issues."""
    return jira_request("POST", "issueLink", {
        "type": {"name": link_type},
        "inwardIssue": {"key": from_key},
        "outwardIssue": {"key": to_key},
    })


def list_strategic_goals(project: str = "PROJGOALS") -> list[dict[str, Any]]:
    """List all strategic goals from the specified project."""
    jql = f'project = {project} AND issuetype = "Strategic Goal" ORDER BY key ASC'
    return search_issues(jql, max_results=100)


def list_outcomes(project: str = "PROJSTRAT", status: str | None = None) -> list[dict[str, Any]]:
    """List existing outcomes from the specified project."""
    jql = f'project = {project} AND issuetype = Outcome'
    if status:
        jql += f' AND status = "{status}"'
    jql += " ORDER BY key ASC"
    return search_issues(jql, max_results=200)


def create_child_issue(parent_key: str, project: str, issue_type: str,
                       summary: str, description: str,
                       labels: list[str] | None = None) -> dict[str, Any]:
    """Create a child issue linked to a parent via 'is child of'."""
    fields: dict[str, Any] = {
        "project": {"key": project},
        "issuetype": {"name": issue_type},
        "summary": summary,
        "description": _text_to_adf(description),
        "parent": {"key": parent_key},
    }

    if labels:
        fields["labels"] = labels

    return jira_request("POST", "issue", {"fields": fields})


def find_outcomes_for_goal(goal_key: str) -> list[dict[str, Any]]:
    """Find outcomes linked to a specific strategic goal."""
    issue = fetch_issue(goal_key)
    outcome_keys = []
    for link in issue.get("fields", {}).get("issuelinks", []):
        linked = link.get("inwardIssue") or link.get("outwardIssue")
        if linked and linked.get("fields", {}).get("issuetype", {}).get("name") == "Outcome":
            outcome_keys.append(linked["key"])
    return [fetch_issue(k) for k in outcome_keys]


def extract_description_text(issue: dict[str, Any]) -> str:
    """Extract plain text from a Jira issue description (handles ADF format)."""
    desc = issue.get("fields", {}).get("description")
    if not desc:
        return ""
    if isinstance(desc, str):
        return desc
    if isinstance(desc, dict):
        return _adf_to_text(desc)
    return str(desc)


def _text_to_adf(text: str) -> dict[str, Any]:
    """Convert plain text/markdown to Atlassian Document Format (simplified)."""
    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": text}],
            }
        ],
    }


def _adf_to_text(adf: dict[str, Any]) -> str:
    """Extract plain text from Atlassian Document Format."""
    parts = []
    for node in adf.get("content", []):
        if node.get("type") == "paragraph":
            for child in node.get("content", []):
                if child.get("type") == "text":
                    parts.append(child.get("text", ""))
            parts.append("\n")
        elif node.get("type") == "heading":
            level = node.get("attrs", {}).get("level", 1)
            prefix = "#" * level + " "
            for child in node.get("content", []):
                if child.get("type") == "text":
                    parts.append(prefix + child.get("text", ""))
            parts.append("\n")
    return "".join(parts).strip()
