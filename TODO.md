# TODO

Deferred items.

## Extend write-mode smoke coverage to every write method

`smoke_test.py --write` exercises a representative subset. Mocked
tests cannot prove server compatibility, so each write method not yet
in the smoke run (chiefly v2 writes and the node/interface/KSC
lifecycle) should be added so the compose-instance run covers the
full write surface.

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

## OpenNMS Discourse announcement

Post in the existing Python REST API thread on the OpenNMS community forum:
<https://opennms.discourse.group/t/python-library-for-rest-api/1387>

Include: PyPI install command, RTD docs link, brief feature summary.
