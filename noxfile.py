"""Developer task automation."""

import nox

nox.options.default_venv_backend = "uv"
nox.options.sessions = [
    "check_format",
    "check_lint",
    "check_types",
    "run_tests",
]

PYTHON = ["3.13"]
CODE_TO_TEST = ["src", "tests", "noxfile.py"]


@nox.session(python=PYTHON)
def run_tests(session: nox.Session):
    """Run unit tests."""
    session.run_install(
        "uv",
        "sync",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
        silent=True,
    )
    pytest_args = session.posargs if session.posargs else []

    session.run(
        "pytest",
        "--cache-clear",
        "--junitxml=junit.xml",
        "--cov-fail-under=90",
        "--cov=src",
        "--cov-branch",
        "--cov-report=term",
        "--cov-report=xml",
        *pytest_args,
    )


@nox.session(python=False)
def check_format(session: nox.Session):
    """Check code formatting."""
    session.run("ruff", "format", *CODE_TO_TEST, "--check")


@nox.session(python=False)
def format(session: nox.Session):
    """Check code formatting and auto fix the errors if possible."""
    session.run("ruff", "format", *CODE_TO_TEST)


@nox.session(python=False)
def check_lint(session: nox.Session):
    """Check code linting."""
    session.run("ruff", "check", *CODE_TO_TEST)


@nox.session(python=False)
def lint(session: nox.Session):
    """Check code linting and auto fix the erros if possible."""
    session.run("ruff", "check", *CODE_TO_TEST, "--fix")


@nox.session(python=False)
def check_types(session: nox.Session):
    """Run static type checking."""
    session.run("mypy", *CODE_TO_TEST)
