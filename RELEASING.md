# Releasing

Each release packages one upstream FVS tag as `fvs-runtime` version `YYYY.N.P.R` where `R` is the packaging revision: 0 for the first release of a tag, then 1, 2, … to repackage the same FVS source.

## Start the release

```sh
gh workflow run release.yml -f source_ref=2027.1.1 -f revision=0
```

Once every wheel is built and verified, the run waits for a reviewer to approve the `pypi` environment.

## Approve or reject

Approving the `pypi` deployment on the run's page publishes the wheels. Before approving, check the run's `source_ref` and `revision`, and read any regression-test diffs in the native build jobs' summaries. Approve only if they look like rounding in the last digit. Rejecting publishes nothing. A fix goes out as the next revision (`-f revision=1`).
