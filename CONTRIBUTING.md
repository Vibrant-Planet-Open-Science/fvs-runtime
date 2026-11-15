# Contributing

fvs-runtime has a purposefully narrow scope: it packages prebuilt FVS shared libraries as wheels and reports where they are installed. Issues and pull requests are welcome when they concern that, such as installing a wheel, a missing platform, library lookup, or build provenance.

For most FVS users, it is unlikely that fvs-runtime is the right place to report unexpected behavior or to make contributions. If you have issues or contributions you'd like to make to the FVS ecosystem, make sure you go to the right place:

- **FVS itself** (simulation results, keywords, crashes inside FVS): [ForestVegetationSimulator](https://github.com/USDAForestService/ForestVegetationSimulator/issues)
- **How the libraries we use in fvs-runtime are compiled** (compiler flags, build failures): [fvs-build](https://github.com/Vibrant-Planet-Open-Science/fvs-build/issues)
- **Running FVS from Python**: [fvs2py](https://github.com/Vibrant-Planet-Open-Science/fvs2py/issues)
- **Running FVS from R**: [rFVS](https://github.com/USDAForestService/ForestVegetationSimulator-Interface/issues)

## How the packages fit together

Each FVS release is published as one distribution, `fvs-runtime`, with one wheel per platform. Each wheel holds all 22 variants' shared libraries in `fvs_runtime/lib/`, their fvs-build provenance in `fvs_runtime/provenance/`, and a few lines of path lookup (`variants()`, `library_path()`, `provenance()`).

No source code is compiled here. For each release, the pack step takes the libraries from fvs-build's bundles, renders the `pyproject.toml` template, builds the wheel, and repairs it (`auditwheel` on Linux, `delocate` as a check on macOS).

## Layout

| Path | What |
| --- | --- |
| `src/fvs_runtime/` | The `fvs-runtime` package: lookup of the installed libraries |
| `templates/` | `pyproject.toml` template the pack step renders for each release |
| `tests/` | Tests of the lookup code against a fake installed `lib/` |

## Development environment

You need [uv](https://docs.astral.sh/uv/) and Python 3.10 or newer. No Fortran compiler or FVS build is needed: the libraries come from fvs-build.

```sh
git clone https://github.com/Vibrant-Planet-Open-Science/fvs-runtime.git
cd fvs-runtime
uv sync --extra dev
uv run pre-commit install
```

The root `pyproject.toml` describes this development environment only (`fvs-runtime-dev`, never published). The published `fvs-runtime` metadata is in `templates/fvs-runtime.pyproject.toml`.

## Tests

```sh
uv run pytest
```

The tests lay out a fake `lib/` and `provenance/` in a temporary directory and point the package at it, so they run without any FVS libraries installed.

## Checks

Hooks run on each commit: a gitleaks secret scan, Ruff (lint with fixes, then format) and mypy on `src/`. Run them on the whole tree with:

```sh
uv run pre-commit run --all-files
```

## Style

Ruff and mypy enforce most of the style. Beyond what they check:

- Docstrings follow the [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
- Mark code in docstrings with single backticks (`` `library_path` ``). Don't use reST roles (`:func:`) or double backticks.

## Commit messages and PR titles

Pull requests are squash-merged, and the PR title becomes the commit message on `main`. Titles follow [Conventional Commits](https://www.conventionalcommits.org/), as in the other FVS repositories:

```
<type>: <lowercase, present-tense summary>
```

For example, `fix: names the missing variant in the lookup error` or `docs: fixes the rFVS example`. Types: `feat`, `fix`, `perf`, `docs`, `build`, `refactor`, `ci`, `test`, `chore`; mark a breaking change with `!` (`feat!: ...`).

Release versions don't come from commit messages: each release is the upstream FVS version plus a packaging revision (`2027.1.0.0`, then `2027.1.0.1` for a repackaging of the same FVS source).
