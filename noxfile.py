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
    "array_api_strict>=2",
    "jax>=0.4.32",
    "pytest",
    "pytest-benchmark",
    "coverage[toml]",
]
GLASS_REPO_URL = "https://github.com/glass-dev/glass"


def _get_revisions_from_posargs(
    posargs: list[str],
    expected_num_revisions: int,
) -> tuple[str, str]:
    first_revision = ""
    second_revision = ""
    if posargs:
        args = posargs
        if len(args) == 1 and expected_num_revisions in {1, 2}:
            first_revision = args[0]
        elif len(args) == expected_num_revisions == 2:  # noqa: PLR2004
            first_revision = args[0]
            second_revision = args[1]
        else:
            msg = (
                f"Incorrect number of revisions provided {len(args)}, "
                f"expected {expected_num_revisions}"
            )
            raise ValueError(msg)
    else:
        msg = "Revision not provided"
        raise ValueError(msg)
    return first_revision, second_revision


def _setup_tests(session: nox.Session) -> None:
    """Install dependencies and extract revision."""
    session.install(*DEPENDENCIES)
    revision = _get_revisions_from_posargs(session.posargs, 1)[0]
    session.install(f"git+{GLASS_REPO_URL}@{revision}")


@nox.session
def lint(session: nox.Session) -> None:
    """Run the linter."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--all-files", *session.posargs)


@nox.session(python=ALL_PYTHON)
def benchmark(session: nox.Session) -> None:
    """Run the benchmarks."""
    _setup_tests(session)
    session.run("pytest", "--benchmark-autosave")


@nox.session(python=ALL_PYTHON)
def coverage(session: nox.Session) -> None:
    """Run tests and compute coverage of glass."""
    _setup_tests(session)
    session.run("coverage", "run", "--source=glass", "-m", "pytest")


@nox.session(python=ALL_PYTHON)
def regression_tests(session: nox.Session) -> None:
    """Run the regression test."""
    session.install(*DEPENDENCIES)

    before_revision, after_revision = _get_revisions_from_posargs(session.posargs, 2)

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
