# TODO

Items deferred for a future session.

## Meridian 2025 coverage gaps — done

All gaps from the audit in `COVERAGE.md`
([#44](https://github.com/cnewkirk/opennms-api-wrapper/issues/44))
were implemented in
[#46](https://github.com/cnewkirk/opennms-api-wrapper/issues/46):
12 new mixins, plus backwards-compatibility annotations on
`MapsMixin` (the maps API was removed upstream in Horizon 16).
`COVERAGE.md` has the current matrix.

## Write-mode smoke tests

`smoke_test.py --write` has not yet been validated against a live server.
The read-only path is validated against Meridian 2024.3.0; write mode
creates and deletes objects (events, categories, groups, requisitions, maps,
etc.) and needs a dedicated dev or staging instance to run safely.

- Run `python smoke_test.py --write --yes` against a non-production server
- Fix any failures, then update the README/docs validation note from
  "write mode untested live" to the confirmed version

## Pre-commit config

Add `.pre-commit-config.yaml` so contributors get ruff feedback before
pushing:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.0   # pin to a recent release
    hooks:
      - id: ruff
```

Update `CONTRIBUTING.md` to mention `pre-commit install` as an optional
setup step.

## Development Status classifier

`pyproject.toml` currently declares `Development Status :: 4 - Beta`.
Consider upgrading to `5 - Production/Stable` once write-mode smoke tests
pass against a live server.

## OpenNMS Discourse announcement

Post in the existing Python REST API thread on the OpenNMS community forum:
<https://opennms.discourse.group/t/python-library-for-rest-api/1387>

Include: PyPI install command, RTD docs link, brief feature summary.
