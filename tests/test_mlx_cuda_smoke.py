"""Smoke tests for MLX running on the CUDA backend.

These tests are intentionally small and dependency-light. They verify that:

* the installed MLX build exposes the CUDA backend,
* at least one GPU device is visible,
* MLX can select the GPU as the default device,
* basic elementwise, reduction, matmul, and softmax operations execute, and
* results can be materialized back on the host with the expected values.

Run with:
    python -m pytest -q tests/test_mlx_cuda_smoke.py

Install example for CUDA 12 hosts:
    python -m pip install "mlx[cuda12]" pytest numpy
"""

from __future__ import annotations

import numpy as np
import pytest

import mlx.core as mx


def _require_cuda_backend() -> None:
    """Skip cleanly unless this MLX install can run CUDA kernels."""

    cuda = getattr(mx, "cuda", None)
    if cuda is None or not hasattr(cuda, "is_available"):
        pytest.skip('MLX CUDA support is not present; install with "mlx[cuda12]" or "mlx[cuda13]".')

    if not cuda.is_available():
        pytest.skip("MLX CUDA backend is not available on this host.")

    try:
        device_count = mx.device_count(mx.gpu)
    except Exception as exc:  # pragma: no cover - this is a smoke-test diagnostic path.
        pytest.fail(f"MLX reports CUDA as available, but GPU device_count failed: {exc!r}")

    assert device_count > 0, "MLX CUDA is available but reports zero GPU devices."


def test_cuda_device_can_be_selected() -> None:
    _require_cuda_backend()

    mx.set_default_device(mx.gpu)
    info = mx.device_info()

    assert isinstance(info, dict)
    assert mx.device_count(mx.gpu) > 0


def test_cuda_basic_array_ops() -> None:
    _require_cuda_backend()
    mx.set_default_device(mx.gpu)

    x = mx.arange(16, dtype=mx.float32).reshape(4, 4)
    y = (x * 2.0 + 1.0).sum()
    mx.eval(y)

    assert float(y.item()) == pytest.approx(256.0)


def test_cuda_matmul() -> None:
    _require_cuda_backend()
    mx.set_default_device(mx.gpu)

    a = mx.arange(9, dtype=mx.float32).reshape(3, 3)
    b = mx.ones((3, 3), dtype=mx.float32)
    c = mx.matmul(a, b)
    mx.eval(c)

    expected = np.array(
        [
            [3.0, 3.0, 3.0],
            [12.0, 12.0, 12.0],
            [21.0, 21.0, 21.0],
        ],
        dtype=np.float32,
    )
    np.testing.assert_allclose(np.array(c), expected, rtol=1e-5, atol=1e-5)


def test_cuda_softmax() -> None:
    _require_cuda_backend()
    mx.set_default_device(mx.gpu)

    logits = mx.array([[1.0, 2.0, 3.0], [1.0, 1.0, 1.0]], dtype=mx.float32)
    probs = mx.softmax(logits, axis=-1)
    mx.eval(probs)

    probs_np = np.array(probs)
    np.testing.assert_allclose(probs_np.sum(axis=-1), np.ones(2), rtol=1e-5, atol=1e-5)
    assert probs_np[0, 2] > probs_np[0, 1] > probs_np[0, 0]
    np.testing.assert_allclose(probs_np[1], np.array([1 / 3, 1 / 3, 1 / 3]), rtol=1e-5, atol=1e-5)
