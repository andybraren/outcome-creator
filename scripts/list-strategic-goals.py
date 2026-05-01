#!/usr/bin/env python3
"""List strategic goals from the PROJGOALS project for use as outcome inputs."""

import argparse
import json
import sys

from jira_utils import extract_description_text, list_strategic_goals


def main():
    parser = argparse.ArgumentParser(description="List strategic goals from Jira")
    parser.add_argument("--project", default="PROJGOALS", help="Jira project key (default: PROJGOALS)")
    parser.add_argument("--format", choices=["json", "table", "keys"], default="table", help="Output format")
    args = parser.parse_args()

    try:
        goals = list_strategic_goals(args.project)
    except Exception as e:
        print(f"Error fetching strategic goals: {e}", file=sys.stderr)
        sys.exit(1)

    if args.format == "keys":
        for g in goals:
            print(g["key"])
        return

    results = []
    for g in goals:
        fields = g.get("fields", {})
        results.append({
            "key": g["key"],
            "summary": fields.get("summary"),
            "status": fields.get("status", {}).get("name"),
            "priority": fields.get("priority", {}).get("name"),
            "description_preview": extract_description_text(g)[:200],
        })

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print(f"{'Key':<20} {'Status':<15} {'Priority':<12} Summary")
        print("-" * 90)
        for r in results:
            print(f"{r['key']:<20} {r['status']:<15} {r['priority']:<12} {r['summary']}")

    print(f"\nTotal: {len(results)} strategic goals", file=sys.stderr)


if __name__ == "__main__":
    main()
