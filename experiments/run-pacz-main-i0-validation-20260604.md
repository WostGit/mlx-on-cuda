# Trigger PACZero main validation run

This file triggers `.github/workflows/pacz-main-i0.yml` on `main` after recommitting the workflow as a first-cell validation run.

Validation target:

- `scripts/headline/sst2_1p3b_lora_paczpl_s1.sh`

Expected output:

- `logs/pacz-main-i0-validation/sst2_1p3b_lora_paczpl_s1/status.json`
- `logs/pacz-main-i0-validation/sst2_1p3b_lora_paczpl_s1/latest.log`
- `logs/pacz-main-i0-validation/sst2_1p3b_lora_paczpl_s1/metrics.json`
