# Contributing

fvs-runtime packages prebuilt FVS shared libraries as wheels and reports where they are installed. Issues and pull requests here should be about that: installing a wheel, a missing platform, library lookup or provenance. Everything else belongs elsewhere:

- FVS itself (results, keywords, crashes): [ForestVegetationSimulator](https://github.com/USDAForestService/ForestVegetationSimulator/issues)
- How the libraries are compiled: [fvs-build](https://github.com/Vibrant-Planet-Open-Science/fvs-build/issues)
- Running FVS from Python: [fvs2py](https://github.com/Vibrant-Planet-Open-Science/fvs2py/issues); from R: [rFVS](https://github.com/USDAForestService/ForestVegetationSimulator-Interface/issues)

## How it works

Nothing is compiled here. fvs-build compiles FVS for each platform, and `.github/workflows/release.yml` packs each platform's shared libraries into a wheel, along with their provenance and fvs-build's SBOM. Pull requests that touch the workflow, `src/`, `templates/` or `tools/` run the same workflow, stopping short of the upload. [RELEASING.md](RELEASING.md) covers publishing a release.

## Layout

| Path | What |
| --- | --- |
| `src/fvs_runtime/` | The `fvs-runtime` package: lookup of the installed libraries |
| `templates/` | `pyproject.toml` template and hatchling hook the pack step stages for each wheel |
| `tests/` | Tests of the lookup code, version mapping and pack step, against fake bundles |
| `tools/` | `pack.py` (one fvs-build bundle to one wheel), `version.py` (upstream tag to wheel version) and `verify.py` (installed wheel against its provenance) |

## Development environment

You need [uv](https://docs.astral.sh/uv/) and Python 3.12 or newer. No Fortran compiler or FVS build is needed: the libraries come from fvs-build.

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

To build a wheel from a real fvs-build bundle, download one (`gh run download <run-id> -n <artifact_name>` in fvs-build) and run:

```sh
uv run python tools/pack.py <bundle-dir> <revision> <platform-tag>   # e.g. 0 linux_x86_64; writes dist/
```

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

Versions follow FVS releases, not commit messages (see [RELEASING.md](RELEASING.md)).
