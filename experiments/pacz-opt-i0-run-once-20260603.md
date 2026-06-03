# Run PACZero I0 smoke once

This is the single exact trigger file for `.github/workflows/pacz-opt-smoke.yml`.

Expected behavior:
- one push to this exact path starts the PACZero OPT-1.3B I=0 smoke workflow;
- workflow log commits under `logs/pacz-opt-i0/` do not match the trigger path;
- no manual dispatch trigger is enabled in this workflow.
