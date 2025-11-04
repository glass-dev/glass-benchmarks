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
GLASS_REPO_URL = "https://github.com/glass-dev/glass"


@nox.session
def lint(session: nox.Session) -> None:
    """Run the linter."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session(python=ALL_PYTHON)
def benchmark(session: nox.Session) -> None:
    """Run the benchmarks."""
    session.install("-e", ".")

    revision = ""
    if session.posargs:
        args = session.posargs
        if len(args) != 1:
            msg = f"Incorrect number of revisions provided {len(args)}"
            raise ValueError(msg)
        revision = args[0]
    else:
        msg = "Revision not provided"
        raise ValueError(msg)

    # Verify revisions have been provided

    print(f"Running benchmark for revision {revision}")
    session.install(f"git+{GLASS_REPO_URL}@{revision}")
    session.run("pytest", "--benchmark-autosave")


@nox.session(python=ALL_PYTHON)
def regression_tests(session: nox.Session) -> None:
    """Run the regression test."""
    session.install("-e", ".")

    before_revision = "main"
    after_revision = ""
    if session.posargs:
        revisions = session.posargs
        if len(revisions) == 1:
            after_revision = revisions[0]
        elif len(revisions) == 2:  # noqa: PLR2004
            before_revision = revisions[0]
            after_revision = revisions[1]
        else:
            msg = f"Incorrect number of revisions provided {len(revisions)}"
            raise ValueError(msg)
    else:
        msg = "No revisions not provided"
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
