#!/usr/bin/env python3
"""Benchmark small Qwen-family models with MLX on CUDA.

The script is designed for CI smoke benchmarking rather than leaderboard-quality
numbers. It records one JSON object per model so failed loads or OOMs are visible
without stopping the whole run.

Environment variables:
    BENCH_MODELS       Comma-separated model ids.
    BENCH_PROMPT       Prompt to generate from.
    BENCH_MAX_TOKENS   Number of generated tokens requested per model.
    BENCH_WARMUP       1 to run a short warmup generation before timing.
    BENCH_OUTPUT       Output JSONL path.
"""

from __future__ import annotations

import gc
import json
import os
import platform
import time
import traceback
from pathlib import Path
from typing import Any

import mlx.core as mx
from mlx_lm import generate, load


DEFAULT_MODELS = [
    "Qwen/Qwen3-0.6B",
    "Qwen/Qwen3-1.7B",
    "Qwen/Qwen2.5-3B-Instruct",
    "Qwen/Qwen3-4B",
    "Qwen/Qwen3-8B",
]

DEFAULT_PROMPT = "Write one concise paragraph explaining why CUDA smoke tests are useful."


def _jsonable(value: Any) -> Any:
    try:
        json.dumps(value)
        return value
    except TypeError:
        return repr(value)


def _device_snapshot() -> dict[str, Any]:
    info: dict[str, Any] = {}
    try:
        info["cuda_available"] = bool(mx.cuda.is_available())
    except Exception as exc:
        info["cuda_available_error"] = repr(exc)

    try:
        info["gpu_device_count"] = int(mx.device_count(mx.gpu))
    except Exception as exc:
        info["gpu_device_count_error"] = repr(exc)

    try:
        info["device_info"] = {k: _jsonable(v) for k, v in mx.device_info().items()}
    except Exception as exc:
        info["device_info_error"] = repr(exc)

    return info


def _token_count(tokenizer: Any, text: str) -> int:
    try:
        encoded = tokenizer.encode(text)
        return len(encoded)
    except Exception:
        return max(1, len(text.split()))


def _clear_mlx() -> None:
    try:
        mx.clear_cache()
    except Exception:
        pass
    gc.collect()


def benchmark_one(model_id: str, prompt: str, max_tokens: int, warmup: bool) -> dict[str, Any]:
    row: dict[str, Any] = {
        "model": model_id,
        "status": "started",
        "max_tokens": max_tokens,
        "prompt_tokens": None,
        "generated_tokens": None,
        "load_seconds": None,
        "generate_seconds": None,
        "tokens_per_second": None,
        "output_preview": None,
        "error": None,
        "traceback": None,
        "device_before": _device_snapshot(),
        "device_after": None,
    }

    model = None
    tokenizer = None
    try:
        mx.set_default_device(mx.gpu)

        load_start = time.perf_counter()
        model, tokenizer = load(model_id)
        row["load_seconds"] = round(time.perf_counter() - load_start, 4)
        row["prompt_tokens"] = _token_count(tokenizer, prompt)

        if warmup:
            _ = generate(model, tokenizer, prompt=prompt, max_tokens=4, verbose=False)
            mx.eval(mx.array([0]))

        gen_start = time.perf_counter()
        output = generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens, verbose=False)
        mx.eval(mx.array([0]))
        gen_seconds = time.perf_counter() - gen_start

        generated_tokens = _token_count(tokenizer, output)
        row["generated_tokens"] = generated_tokens
        row["generate_seconds"] = round(gen_seconds, 4)
        row["tokens_per_second"] = round(generated_tokens / gen_seconds, 4) if gen_seconds > 0 else None
        row["output_preview"] = output[:500]
        row["status"] = "ok"
    except Exception as exc:  # Keep benchmarking the remaining models.
        row["status"] = "error"
        row["error"] = repr(exc)
        row["traceback"] = traceback.format_exc()
    finally:
        row["device_after"] = _device_snapshot()
        del model
        del tokenizer
        _clear_mlx()

    return row


def main() -> int:
    models = [m.strip() for m in os.environ.get("BENCH_MODELS", ",".join(DEFAULT_MODELS)).split(",") if m.strip()]
    prompt = os.environ.get("BENCH_PROMPT", DEFAULT_PROMPT)
    max_tokens = int(os.environ.get("BENCH_MAX_TOKENS", "64"))
    warmup = os.environ.get("BENCH_WARMUP", "1") not in {"0", "false", "False", "no", "No"}
    output_path = Path(os.environ.get("BENCH_OUTPUT", "logs/mlx-model-benchmark/latest.jsonl"))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    header = {
        "kind": "metadata",
        "utc_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "models": models,
        "max_tokens": max_tokens,
        "warmup": warmup,
        "device": _device_snapshot(),
    }

    failures = 0
    with output_path.open("w", encoding="utf-8") as f:
        print(json.dumps(header, sort_keys=True), file=f, flush=True)
        print(json.dumps(header, indent=2, sort_keys=True), flush=True)

        for model_id in models:
            print(f"\n=== Benchmarking {model_id} ===", flush=True)
            row = benchmark_one(model_id, prompt, max_tokens, warmup)
            print(json.dumps(row, sort_keys=True), file=f, flush=True)
            print(json.dumps(row, indent=2, sort_keys=True), flush=True)
            if row["status"] != "ok":
                failures += 1

    summary = {
        "kind": "summary",
        "models_total": len(models),
        "models_ok": len(models) - failures,
        "models_failed": failures,
        "output_path": str(output_path),
    }
    print(json.dumps(summary, indent=2, sort_keys=True), flush=True)

    # Return success if at least one model benchmarked successfully. This lets the
    # workflow commit partial results while still flagging total failure.
    return 0 if failures < len(models) else 1


if __name__ == "__main__":
    raise SystemExit(main())
