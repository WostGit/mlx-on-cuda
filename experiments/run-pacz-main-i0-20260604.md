# Trigger PACZero I=0 reproduction on main

This file triggers `.github/workflows/pacz-main-i0.yml` on the `main` branch.

Setup:

- existing MLX smoke workflow ignores this trigger file;
- existing MLX model benchmark workflow ignores this trigger file;
- PACZero runs as sequential per-cell matrix jobs;
- each cell uses portable `timeout ... 330m`;
- per-cell output is under `logs/pacz-main-i0/<cell_id>/`;
- aggregate output is under `logs/pacz-main-i0/summary/latest.json`.
