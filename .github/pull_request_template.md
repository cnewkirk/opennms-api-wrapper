## Summary

<!-- What does this PR do? -->

## Checklist

- [ ] `pytest tests/ -v` passes locally
- [ ] `ruff check opennms_api_wrapper/` passes
- [ ] `mypy opennms_api_wrapper/types.py` passes
- [ ] New or changed methods have corresponding tests in `tests/`
- [ ] New fixture shapes added to `tests/fixtures.py` if needed
- [ ] Write-method payloads have a `TypedDict` in `types.py`
- [ ] No new runtime dependencies introduced
