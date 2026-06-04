# Trigger PACZero reset I=0 reproduction

This file triggers the clean reset workflow `.github/workflows/pacz-reset-i0.yml` on branch `experiment/pacz-reset-20260604`.

Reset design:

- branch was created fresh from the clean base commit;
- generic MLX CUDA smoke ignores this branch;
- MLX model benchmark ignores this branch;
- PACZero runs as sequential per-cell matrix jobs;
- each cell uses portable `timeout ... 330m`;
- per-cell output is under `logs/pacz-reset-i0/<cell_id>/`;
- aggregate output is under `logs/pacz-reset-i0/summary/latest.json`.
