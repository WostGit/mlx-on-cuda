# Trigger clean PACZero I=0 full reproduction

This exact file path triggers `.github/workflows/pacz-i0-full-clean.yml` once on branch `experiment/pacz-i0-full-clean-20260603`.

The workflow reproduces the OPT-1.3B PAC-ZPL / I=0 Table 1 cells:

- SST-2 LoRA seeds 1, 2, 3
- SST-2 full-parameter seeds 0, 1, 2
- SQuAD LoRA seed 0
- SQuAD full-parameter seeds 0, 1, 2

Logs and metrics are committed under `logs/pacz-i0-full-clean/`, which does not match this trigger path.
