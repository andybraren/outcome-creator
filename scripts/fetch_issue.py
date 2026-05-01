#!/usr/bin/env python3
"""Fetch a Jira issue and print its key fields as JSON. REST API fallback for when MCP is unavailable."""

import argparse
import json
import sys

from jira_utils import extract_description_text, fetch_issue


def main():
    parser = argparse.ArgumentParser(description="Fetch a Jira issue by key")
    parser.add_argument("key", help="Jira issue key (e.g., PROJSTRAT-1344)")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="Output format")
    args = parser.parse_args()

    try:
        issue = fetch_issue(args.key)
    except Exception as e:
        print(f"Error fetching {args.key}: {e}", file=sys.stderr)
        sys.exit(1)

    fields = issue.get("fields", {})
    result = {
        "key": issue.get("key"),
        "summary": fields.get("summary"),
        "description": extract_description_text(issue),
        "status": fields.get("status", {}).get("name"),
        "priority": fields.get("priority", {}).get("name"),
        "issue_type": fields.get("issuetype", {}).get("name"),
        "components": [c.get("name") for c in fields.get("components", [])],
        "labels": fields.get("labels", []),
        "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
        "reporter": fields.get("reporter", {}).get("displayName") if fields.get("reporter") else None,
        "created": fields.get("created"),
        "updated": fields.get("updated"),
    }

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Key: {result['key']}")
        print(f"Summary: {result['summary']}")
        print(f"Status: {result['status']}")
        print(f"Priority: {result['priority']}")
        print(f"Type: {result['issue_type']}")
        print(f"Components: {', '.join(result['components'])}")
        print(f"Labels: {', '.join(result['labels'])}")
        print(f"\nDescription:\n{result['description']}")


if __name__ == "__main__":
    main()
