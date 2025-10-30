from __future__ import annotations

from typing import TYPE_CHECKING

import jax.numpy as jnp
import numpy as np
import pytest

import array_api_strict

if TYPE_CHECKING:
    from types import ModuleType

xp_available_backends: dict[str, ModuleType] = {
    "array_api_strict": array_api_strict,
    "numpy": np,
    "jax.numpy": jnp,
}


@pytest.fixture(params=xp_available_backends.values(), scope="session")
def xp(request: pytest.FixtureRequest) -> ModuleType:
    """
    Fixture for array backend.

    Access array library functions using `xp.` in tests.
    """
    return request.param  # type: ignore[no-any-return]
