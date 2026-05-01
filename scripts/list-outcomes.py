#!/usr/bin/env python3
"""List existing outcomes from the PROJSTRAT project."""

import argparse
import json
import sys

from jira_utils import list_outcomes


def main():
    parser = argparse.ArgumentParser(description="List existing outcomes from Jira")
    parser.add_argument("--project", default="PROJSTRAT", help="Jira project key (default: PROJSTRAT)")
    parser.add_argument("--status", help="Filter by status (e.g., 'In Progress', 'New')")
    parser.add_argument("--format", choices=["json", "table", "keys"], default="table", help="Output format")
    args = parser.parse_args()

    try:
        outcomes = list_outcomes(args.project, args.status)
    except Exception as e:
        print(f"Error fetching outcomes: {e}", file=sys.stderr)
        sys.exit(1)

    if args.format == "keys":
        for o in outcomes:
            print(o["key"])
        return

    results = []
    for o in outcomes:
        fields = o.get("fields", {})
        labels = fields.get("labels", [])
        has_score = any(l.startswith("outcome-creator-") for l in labels)
        results.append({
            "key": o["key"],
            "summary": fields.get("summary"),
            "status": fields.get("status", {}).get("name"),
            "priority": fields.get("priority", {}).get("name"),
            "components": [c.get("name") for c in fields.get("components", [])],
            "scored": has_score,
        })

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print(f"{'Key':<20} {'Status':<15} {'Priority':<10} {'Scored':<8} Summary")
        print("-" * 100)
        for r in results:
            scored = "Yes" if r["scored"] else ""
            print(f"{r['key']:<20} {r['status']:<15} {r['priority']:<10} {scored:<8} {r['summary']}")

    print(f"\nTotal: {len(results)} outcomes", file=sys.stderr)


if __name__ == "__main__":
    main()
