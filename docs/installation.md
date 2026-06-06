# Installation & Testing

## Installation

**From PyPI**

    $ pip install herepy
    $ uv pip install herepy

**From source**

Install dependencies using `uv`

```console
$ uv sync
```

Download the latest `herepy` library from: https://github.com/abdullahselek/HerePy

To install the project in editable mode for development:

```console
$ uv sync
```

## Running Tests

The test suite can be run against a single Python version using `uv`

To run the unit tests with a single Python version

```console
$ uv run pytest -v
```

to also run code coverage

```console
$ uv run pytest -v --cov-report html --cov=herepy
```

To run the unit tests against a set of Python versions::

```console
$ tox
```

## Getting the code

The code is hosted at [Github](https://github.com/abdullahselek/HerePy).

Check out the latest development version anonymously with

```console
$ git clone https://github.com/abdullahselek/HerePy.git
$ cd HerePy
```
