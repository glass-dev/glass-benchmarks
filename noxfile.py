"""Nox config."""

import os

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
BEFORE_REVISION = "main"
GLASS_REPO_URL = "https://github.com/glass-dev/glass"


@nox.session
def lint(session: nox.Session) -> None:
    """Run the linter."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session(python=ALL_PYTHON)
def regression_tests(session: nox.Session) -> None:
    """Run the regression test."""
    session.install("-e", ".")

    # Verify revisions have been provided
    before_revision = os.environ.get("BEFORE_REVISION")
    before_revision = before_revision if before_revision else "main"

    after_revision = os.environ.get("AFTER_REVISION")
    if not after_revision:
        msg = "'AFTER_REVISION' not provided"
        raise ValueError(msg)

    print(f"Generating before benchmark for comparison from revision {BEFORE_REVISION}")
    session.install(f"git+{GLASS_REPO_URL}@{BEFORE_REVISION}")
    session.run("pytest", "--benchmark-autosave", *session.posargs)

    print(f"Comparing before benchmark to revisiob {after_revision}")
    session.install(f"git+{GLASS_REPO_URL}@{after_revision}")
    session.run(
        "pytest",
        "--benchmark-compare=0001",
        "--benchmark-compare-fail=min:5%",
        *session.posargs,
    )
