from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import jax.numpy
import numpy as np
import pytest

import array_api_strict

import glass.jax

if TYPE_CHECKING:
    from types import ModuleType
    from typing import TypeAlias

    UnifiedGenerator: TypeAlias = (
        np.random.Generator | glass.jax.Generator | glass._array_api_utils.Generator  # noqa: SLF001
    )


# Change jax logger to only log ERROR or worse
logging.getLogger("jax").setLevel(logging.ERROR)


xp_available_backends: dict[str, ModuleType] = {
    "array_api_strict": array_api_strict,
    "numpy": np,
    "jax.numpy": jax.numpy,
}


@pytest.fixture(params=xp_available_backends.values(), scope="session")
def xp(request: pytest.FixtureRequest) -> ModuleType:
    """
    Fixture for array backend.

    Access array library functions using `xp.` in tests.
    """
    return request.param  # type: ignore[no-any-return]


@pytest.fixture(scope="session")
def urng(xp: ModuleType) -> UnifiedGenerator:
    """
    Fixture for a unified RNG interface.

    Access the relevant RNG using `urng.` in tests.

    Must be used with the `xp` fixture. Use `rng` for non array API tests.
    """
    seed = 42
    backend = xp.__name__
    if backend == "jax.numpy":
        return glass.jax.Generator(seed=seed)
    if backend == "numpy":
        return np.random.default_rng(seed=seed)
    if backend == "array_api_strict":
        return glass._array_api_utils.Generator(seed=seed)  # noqa: SLF001
    msg = "the array backend in not supported"
    raise NotImplementedError(msg)
