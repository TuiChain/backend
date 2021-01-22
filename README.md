<!-- ----------------------------------------------------------------------- -->

# TuiChain: Backend

[![Build status](https://github.com/TuiChain/backend/workflows/build/badge.svg?branch=main)](https://github.com/TuiChain/backend/actions)

Repository for the backend component of the TuiChain application.

## Development setup

Create a virtualenv and install the dependencies in `requirements-dev.txt`, *e.g.*:

- `virtualenv venv`
- `source venv/bin/activate`
- `pip install pip==20.2.3`
- `pip install --use-feature=2020-resolver -r requirements-dev.txt`

You will likely need to have a nightly version of the Rust compiler installed.
Install rustup by following the instructions at https://www.rust-lang.org/tools/install and then run `rustup default nightly`.

A full test configuration is included in file `.env_test`.
Copy it to `.env` to use it.

## Formatting code

Run `black .` in the repo's root.

<!-- ----------------------------------------------------------------------- -->
