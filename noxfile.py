"""Nox config."""

import nox

# Options to modify nox behaviour
nox.options.default_venv_backend = "uv|virtualenv"
nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = [
    "tests",
]

ALL_PYTHON = [
    "3.10",
    "3.11",
    "3.12",
    "3.13",
]
DEPENDENCIES = [
    "array-api-compat",
    "array-api-extra",
    "array-api-strict>=2",
    "healpix",
    "healpy",
    "jax>=0.4.32",
    "pytest",
    "pytest-benchmark",
    "pytest-cov",
    "transformcl",
]
GLASS_REPO_URL = "https://github.com/glass-dev/glass"


@nox.session
def lint(session: nox.Session) -> None:
    """Run the linter."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session(python=ALL_PYTHON)
def benchmark(session: nox.Session) -> None:
    """Run the benchmarks."""
    session.install(*DEPENDENCIES)

    if not session.posargs:
        msg = "Revision not provided"
        raise ValueError(msg)

    if len(session.posargs) == 1:
        revision = session.posargs[0]
    else:
        msg = (
            f"Incorrect number of revisions provided ({len(session.posargs)}), "
            f"expected 2"
        )
        raise ValueError(msg)

    session.install(f"git+{GLASS_REPO_URL}@{revision}")
    session.run("pytest", "--benchmark-autosave")


@nox.session(python=ALL_PYTHON)
def coverage(session: nox.Session) -> None:
    """Run tests and compute coverage of glass."""
    session.install(*DEPENDENCIES)
    session.run(
        "pytest",
        "--cov",
        env={"PYTHONPATH": "glass"},
    )


@nox.session(python=ALL_PYTHON)
def regression_tests(session: nox.Session) -> None:
    """Run the regression test."""
    session.install(*DEPENDENCIES)

    if not session.posargs:
        msg = "Revision not provided"
        raise ValueError(msg)

    if len(session.posargs) == 2:  # noqa: PLR2004
        before_revision, after_revision = session.posargs
    else:
        msg = (
            f"Incorrect number of revisions provided ({len(session.posargs)}), "
            f"expected 2"
        )
        raise ValueError(msg)

    print(f"Generating before benchmark for comparison from revision {before_revision}")
    session.install(f"git+{GLASS_REPO_URL}@{before_revision}")
    session.run("pytest", "--benchmark-autosave")

    print(f"Comparing before benchmark to revisiob {after_revision}")
    session.install(f"git+{GLASS_REPO_URL}@{after_revision}")
    session.run(
        "pytest",
        "--benchmark-compare=0001",
        "--benchmark-compare-fail=min:5%",
    )
