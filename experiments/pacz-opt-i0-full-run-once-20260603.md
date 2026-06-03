# Run PACZero 1.3B I=0 full reproduction once

This is the single exact trigger file for `.github/workflows/pacz-opt-i0-full.yml`.

The workflow runs the OPT-1.3B PAC-ZPL / MI-identically-zero reproduction set from PACZero Table 1:

- SST-2 LoRA seeds 1, 2, 3
- SST-2 full-parameter seeds 0, 1, 2
- SQuAD LoRA seed 0
- SQuAD full-parameter seeds 0, 1, 2

Log commits are written under `logs/pacz-opt-i0-full/`, which does not match the workflow trigger path.
