# Trigger PACZero I=0 full reproduction v2

This exact file path triggers the revised per-cell matrix workflow `.github/workflows/pacz-i0-full-clean.yml` on branch `experiment/pacz-i0-full-clean-20260603`.

Revision notes:

- Each OPT-1.3B PAC-ZPL / I=0 paper cell runs as its own matrix job.
- Jobs run sequentially with `max-parallel: 1` for the single RTX 4080 runner.
- Each cell uses a 5h30m command-level timeout so logs are committed before platform cancellation.
- `continue-on-error: true` and `fail-fast: false` allow later cells and aggregation to continue.
- Per-cell logs, status, and metrics are committed under `logs/pacz-i0-full-clean-v2/<cell_id>/`.
- Aggregate summary is committed under `logs/pacz-i0-full-clean-v2/summary/latest.json`.
