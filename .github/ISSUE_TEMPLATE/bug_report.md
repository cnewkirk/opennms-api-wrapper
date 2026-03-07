---
name: Bug report
about: Something is broken or returning unexpected results
labels: bug
---

**Describe the bug**
A clear description of what is wrong.

**Method called**
Which client method triggered the issue (e.g. `client.get_alarms()`)?

**OpenNMS version**
What version of OpenNMS are you running?

**Expected behaviour**
What did you expect to happen?

**Actual behaviour**
What happened instead? Include the full traceback if there is one.

**Minimal reproduction**
```python
import opennms_api_wrapper as opennms
client = opennms.OpenNMS(...)
# ...
```
