#!/usr/bin/env python3
"""Generate an HTML report from outcome pipeline artifacts."""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from frontmatter import read_frontmatter

PROJECT_ROOT = Path(__file__).parent.parent
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"


def collect_outcomes(directory: Path) -> list[dict]:
    """Read all outcome files and collect their metadata."""
    outcomes = []
    tasks_dir = directory / "outcome-tasks"
    if not tasks_dir.exists():
        return outcomes

    for path in sorted(tasks_dir.glob("*.md")):
        fm, body = read_frontmatter(path)
        if not fm:
            continue

        score = fm.get("score", {})
        outcomes.append({
            "id": fm.get("id", path.stem),
            "title": fm.get("title", "Untitled"),
            "status": fm.get("status", "unknown"),
            "priority": fm.get("priority", ""),
            "strategic_goals": fm.get("strategic_goals", []),
            "components": fm.get("components", []),
            "score": score if isinstance(score, dict) else {},
            "file": str(path),
        })

    return outcomes


def generate_html(outcomes: list[dict], output_path: Path) -> None:
    """Generate an HTML report from outcome data."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total = len(outcomes)
    scored = [o for o in outcomes if o["score"]]
    passed = [o for o in scored if o["score"].get("verdict") == "PASS"]
    revised = [o for o in scored if o["score"].get("verdict") == "REVISE"]
    reworked = [o for o in scored if o["score"].get("verdict") == "REWORK"]

    rows = ""
    for o in outcomes:
        s = o["score"]
        verdict = s.get("verdict", "—")
        verdict_class = {"PASS": "pass", "REVISE": "revise", "REWORK": "rework"}.get(verdict, "")
        total_score = s.get("total", "—")

        rows += f"""
        <tr>
            <td>{o['id']}</td>
            <td>{o['title']}</td>
            <td>{o['priority']}</td>
            <td>{s.get('measurability', '—')}</td>
            <td>{s.get('user_focus', '—')}</td>
            <td>{s.get('business_alignment', '—')}</td>
            <td>{s.get('actionability', '—')}</td>
            <td><strong>{total_score}</strong></td>
            <td class="{verdict_class}">{verdict}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Outcome Creator Pipeline Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 2rem; color: #1a1a1a; }}
        h1 {{ color: #2c3e50; }}
        .summary {{ display: flex; gap: 1rem; margin: 1rem 0 2rem; }}
        .stat {{ background: #f8f9fa; border-radius: 8px; padding: 1rem 1.5rem; text-align: center; }}
        .stat .number {{ font-size: 2rem; font-weight: bold; }}
        .stat .label {{ font-size: 0.85rem; color: #666; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #dee2e6; padding: 0.5rem 0.75rem; text-align: left; }}
        th {{ background: #f8f9fa; font-weight: 600; }}
        .pass {{ color: #28a745; font-weight: bold; }}
        .revise {{ color: #ffc107; font-weight: bold; }}
        .rework {{ color: #dc3545; font-weight: bold; }}
        .timestamp {{ color: #999; font-size: 0.85rem; margin-top: 2rem; }}
    </style>
</head>
<body>
    <h1>Outcome Creator Pipeline Report</h1>

    <div class="summary">
        <div class="stat"><div class="number">{total}</div><div class="label">Total</div></div>
        <div class="stat"><div class="number">{len(scored)}</div><div class="label">Scored</div></div>
        <div class="stat"><div class="number pass">{len(passed)}</div><div class="label">Pass</div></div>
        <div class="stat"><div class="number revise">{len(revised)}</div><div class="label">Revise</div></div>
        <div class="stat"><div class="number rework">{len(reworked)}</div><div class="label">Rework</div></div>
    </div>

    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Priority</th>
                <th>Meas.</th>
                <th>User</th>
                <th>Biz</th>
                <th>Action</th>
                <th>Total</th>
                <th>Verdict</th>
            </tr>
        </thead>
        <tbody>{rows}
        </tbody>
    </table>

    <p class="timestamp">Generated: {now}</p>
</body>
</html>"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"Report written to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate HTML report from outcome artifacts")
    parser.add_argument("--dir", default=str(ARTIFACTS_DIR), help="Artifacts directory")
    parser.add_argument("--output", default=str(ARTIFACTS_DIR / "pipeline-report.html"), help="Output HTML path")
    parser.add_argument("--format", choices=["html", "json"], default="html", help="Output format")
    args = parser.parse_args()

    outcomes = collect_outcomes(Path(args.dir))

    if not outcomes:
        print("No outcome files found.", file=sys.stderr)
        sys.exit(0)

    if args.format == "json":
        print(json.dumps(outcomes, indent=2))
    else:
        generate_html(outcomes, Path(args.output))


if __name__ == "__main__":
    main()
