# Trigger PACZero I=0 full reproduction v5

This exact file path triggers `.github/workflows/pacz-i0-full-clean.yml` after fixing the timeout syntax.

Fix:

- Replaced invalid GNU timeout interval `5h30m` with portable `330m`.
- Per-cell output is now under `logs/pacz-i0-full-clean-v5/<cell_id>/`.
- Aggregate output is under `logs/pacz-i0-full-clean-v5/summary/latest.json`.

Unrelated MLX smoke and MLX model benchmark workflows already ignore this branch.
