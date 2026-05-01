#!/usr/bin/env python3
"""Pull an outcome from Jira into the local/ workspace for human review."""

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

from frontmatter import write_frontmatter
from jira_utils import extract_description_text, fetch_issue

PROJECT_ROOT = Path(__file__).parent.parent
LOCAL_DIR = PROJECT_ROOT / "local"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug[:60]


def parse_sections(description: str) -> dict[str, str]:
    """Parse an outcome description into sections by markdown headings."""
    sections = {}
    current_heading = None
    current_content = []

    for line in description.split("\n"):
        heading_match = re.match(r"^##\s+(.+)$", line)
        if heading_match:
            if current_heading:
                sections[current_heading] = "\n".join(current_content).strip()
            current_heading = heading_match.group(1)
            current_content = []
        else:
            current_content.append(line)

    if current_heading:
        sections[current_heading] = "\n".join(current_content).strip()

    return sections


def main():
    parser = argparse.ArgumentParser(description="Pull an outcome from Jira into local/")
    parser.add_argument("key", help="Jira issue key (e.g., PROJSTRAT-1234)")
    args = parser.parse_args()

    print(f"Fetching {args.key} from Jira...")
    try:
        issue = fetch_issue(args.key)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    fields = issue.get("fields", {})
    summary = fields.get("summary", "Untitled")
    description = extract_description_text(issue)
    slug = slugify(summary)

    fm = {
        "id": args.key,
        "title": summary,
        "status": fields.get("status", {}).get("name", "draft").lower(),
        "strategic_goals": [],
        "components": [c.get("name") for c in fields.get("components", [])],
        "priority": fields.get("priority", {}).get("name", "Major"),
        "labels": fields.get("labels", []),
        "score": None,
        "created": fields.get("created", "")[:10],
        "updated": str(date.today()),
        "jira_url": f"{fields.get('self', '').split('/rest/')[0]}/browse/{args.key}" if fields.get("self") else "",
    }

    for link in fields.get("issuelinks", []):
        linked = link.get("outwardIssue") or link.get("inwardIssue")
        if linked and linked["key"].startswith("PROJGOALS"):
            fm["strategic_goals"].append(linked["key"])

    outcome_path = LOCAL_DIR / "outcome-tasks" / f"{args.key}-{slug}.md"
    outcome_path.parent.mkdir(parents=True, exist_ok=True)
    write_frontmatter(outcome_path, fm, f"\n# {summary}\n\n{description}\n")
    print(f"  Written to: {outcome_path}")

    for subdir in ("outcome-reviews", "outcome-originals"):
        src_dir = ARTIFACTS_DIR / subdir
        dst_dir = LOCAL_DIR / subdir
        if src_dir.exists():
            for f in src_dir.glob(f"{args.key}*"):
                dst = dst_dir / f.name
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
                print(f"  Copied: {f.name} → local/{subdir}/")

    has_pass = "outcome-creator-rubric-pass" in fm.get("labels", [])
    has_attention = "outcome-creator-needs-attention" in fm.get("labels", [])

    print(f"\n  Status: {fm['status']}")
    if has_pass:
        print("  Verdict: PASS — ready for /outcome.signoff")
    elif has_attention:
        print("  Verdict: NEEDS ATTENTION — use /outcome.refine then /outcome.push")
    else:
        print("  Not yet scored — use /outcome.review")


if __name__ == "__main__":
    main()
