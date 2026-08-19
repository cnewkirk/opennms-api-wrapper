# opennms-api-wrapper (renamed to python-opennms)

This project has been **renamed to
[python-opennms](https://pypi.org/project/python-opennms/)**.

`opennms-api-wrapper` 0.6.0 is a transitional shim: it depends on
`python-opennms` and re-exports the `opennms` package under the old
`opennms_api_wrapper` module name with a `DeprecationWarning`.
Existing installs and requirement pins keep working, but no further
releases will be published under this name.

Please switch:

```bash
pip install python-opennms
```

```python
import opennms  # was: import opennms_api_wrapper as opennms
```

- Repository: <https://github.com/cnewkirk/python-opennms>
- Documentation: <https://python-opennms.readthedocs.io/>
