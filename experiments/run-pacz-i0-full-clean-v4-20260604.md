# Trigger PACZero I=0 full reproduction v4

This exact file path triggers `.github/workflows/pacz-i0-full-clean.yml` after disabling unrelated workflows on branch `experiment/pacz-i0-full-clean-20260603`.

Fixes applied before this trigger:

- generic MLX CUDA smoke ignores this branch;
- MLX model benchmark ignores this branch;
- PACZero workflow uses per-cell matrix jobs;
- each cell commits logs and status independently;
- per-cell output is under `logs/pacz-i0-full-clean-v4/<cell_id>/`;
- aggregate output is under `logs/pacz-i0-full-clean-v4/summary/latest.json`.
