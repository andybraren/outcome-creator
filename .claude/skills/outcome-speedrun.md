# /outcome.speedrun

Full outcome pipeline end-to-end with minimal interaction.

## Trigger

User says `/outcome.speedrun` optionally followed by:
- A problem statement or strategic theme
- A Jira key (e.g., `PROJSTRAT-1344`) to fetch and improve an existing outcome
- `--strategic-goal PROJGOALS-XXX` to anchor to a specific strategic goal
- `--input batch.yaml` to process multiple outcomes from a YAML file
- `--headless` to run non-interactively (for CI)
- `--dry-run` to skip Jira writes
- `--batch-size N` to control batch processing (default: 5)
- `--announce-complete` to print completion marker for CI

## Behavior

### Single Outcome (from prompt or Jira key)

1. **Create or Fetch**: If a Jira key is provided, fetch the existing outcome. Otherwise, run `outcome-create` with the provided prompt. Create invokes `/outcome.jtbd-lookup` when `knowledge/jtbd-registry/` is synced.
2. **Refine**: Run `outcome-refine` on the created/fetched outcome.
3. **Review**: Run `outcome-review` with `--auto-revise` enabled. This scores and auto-fixes (up to 2 cycles).
4. **Submit**: If not `--dry-run`, run `outcome-submit` to create/update in Jira.
5. **Report**: Print summary with scores and Jira URL.

### Batch Mode (from YAML file)

1. Read the YAML input file. Each entry has:
   - `prompt` (required): Problem statement or need description
   - `strategic_goal` (optional): PROJGOALS key
   - `research_sources` (optional): Array of research data references. For the JTBD registry use `type: jtbd_registry` with `jobs`, `personas`, `phase`, and/or `auto_match` (see `examples/batch-with-jtbd.yaml`)
   - `priority` (optional): Critical | Major | Minor
   - `components` (optional): Array of component names
2. For each entry with `jtbd_registry` research sources, pass selectors to `/outcome.jtbd-lookup` before create.
3. Process entries in batches of `--batch-size` (default 5).
4. For each entry, run the single-outcome pipeline (create → refine → review → submit).
5. Generate a batch report at `artifacts/pipeline-report.html`.

### Existing Jira Outcome

When a Jira key is provided:
1. Fetch the issue from Jira
2. Convert to outcome document format
3. Run refine → review → submit (update)
4. This is useful for improving outcomes that were manually created in Jira

## Flag Persistence

Parsed arguments are written to `tmp/speedrun-config.yaml` so they survive context compression during long batch runs.

## Output

- Outcome documents in `artifacts/outcome-tasks/`
- Review files in `artifacts/outcome-reviews/`
- Pipeline report at `artifacts/pipeline-report.html` (batch mode)
- Console summary with scores and Jira URLs
- If `--announce-complete`: prints `FULL RUN COMPLETE` marker

## Error Handling

- If create fails: Skip and continue (batch mode) or report error (single mode)
- If review fails: Save the outcome as-is with `outcome-creator-needs-attention` label
- If submit fails: Save locally and report the error; outcome can be submitted manually later
