# Trigger PACZero I=0 full reproduction v3

This trigger is used after disabling the generic MLX CUDA smoke workflow on branch `experiment/pacz-i0-full-clean-20260603`.

Expected behavior:

- only the PACZero per-cell matrix workflow should run;
- the generic MLX CUDA smoke workflow should ignore this branch;
- per-cell logs are written under `logs/pacz-i0-full-clean-v2/<cell_id>/`;
- aggregate summary is written under `logs/pacz-i0-full-clean-v2/summary/latest.json`.
