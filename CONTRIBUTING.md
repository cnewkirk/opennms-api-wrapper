# Contributing

Bug reports and pull requests are welcome.

## Development setup

```bash
git clone https://github.com/cnewkirk/python3-opennms.git
cd python3-opennms
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running the tests

```bash
pytest tests/ -v
```

All 290 tests should pass. CI runs the suite against Python 3.8–3.13 on
every push and pull request.

## Adding a new endpoint

1. Find the appropriate mixin file in `opennms_api_wrapper/` (or create a
   new one following the existing pattern).
2. Add the method using `self._get`, `self._post`, `self._put`, or
   `self._delete`. Pass `v2=True` for `/api/v2/` endpoints.
3. If you created a new mixin, import and add it to the inheritance list in
   `client.py`.
4. Add a corresponding test in `tests/test_<mixin>.py`. Mock the HTTP call
   with `@responses.activate` and add any new fixture shapes to
   `tests/fixtures.py`.

## Style

- PEP 8 throughout: 79-character line limit, 4-space indentation.
- JSON only for request bodies — no XML.
- No new runtime dependencies beyond `requests`.

## Submitting a pull request

1. Fork the repo and create a branch from `main`.
2. Make your changes and ensure `pytest tests/ -v` passes locally.
3. Open a pull request — CI will run automatically.
