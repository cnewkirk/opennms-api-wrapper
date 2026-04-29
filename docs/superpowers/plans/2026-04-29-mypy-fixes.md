# mypy Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix all 427 mypy errors so `mypy opennms_api_wrapper/` exits 0 while keeping `pytest tests/ -v` green.

**Architecture:** Four mechanical change types applied across ~50 files. The biggest fix (321 `attr-defined` errors) is solved by making each mixin inherit from `_OpenNMSBase` — Python's MRO handles the resulting diamond inheritance in `client.py` correctly. The other three fixes are type-annotation cleanups.

**Tech Stack:** Python 3.8+, mypy, `typing.Optional`, `typing.Any`, `types-requests`

---

## Error categories

| Code | Count | Fix |
|------|-------|-----|
| `attr-defined` | 321 | `class FooMixin(_OpenNMSBase):` + `from ._base import _OpenNMSBase` |
| `no_implicit_optional` | 89 | `param: str = None` → `param: Optional[str] = None` |
| `str↔int assignment` | 14 | `params: dict[str, Any] = {...}` explicit annotation |
| `import-untyped` | 3 | Add `types-requests` to dev deps |

---

## Shared pattern reference

Every mixin that triggers `attr-defined` needs these two changes — the rest of the file is untouched:

```python
# 1. Add after the module docstring (before any existing imports):
from ._base import _OpenNMSBase

# 2. Change the class definition line:
class FooMixin(_OpenNMSBase):   # was: class FooMixin:
```

For `no_implicit_optional`, add/extend the typing import and annotate the parameter:

```python
from typing import Any, Optional   # add to existing import or create new one

def method(self, param: str = None, ...):     # before
def method(self, param: Optional[str] = None, ...):  # after
```

For `str↔int` dict assignment, add an explicit annotation at the dict literal:

```python
params: dict[str, Any] = {"limit": limit, "offset": offset}   # was: params = {...}
```

---

## Task 1: pyproject.toml + _base.py

**Files:**
- Modify: `pyproject.toml`
- Modify: `opennms_api_wrapper/_base.py`

- [ ] **Add `types-requests` to dev deps**

  In `pyproject.toml`, change:
  ```toml
  dev = ["pytest", "pytest-cov", "responses", "mkdocs-material", "mkdocstrings[python]", "ruff", "mypy"]
  ```
  to:
  ```toml
  dev = ["pytest", "pytest-cov", "responses", "mkdocs-material", "mkdocstrings[python]", "ruff", "mypy", "types-requests"]
  ```

- [ ] **Install the new dep**

  ```bash
  pip install -e ".[dev]" -q
  ```

- [ ] **Fix `_base.py` — add Optional import and annotate params**

  Add `from typing import Any, Optional` after the existing imports (after line 10, before the `from ._exceptions` block — or just append it):

  ```python
  from typing import Any, Optional
  ```

  Then fix the three helper signatures that use `params: dict = None` (lines ~109, 147, 154) and the `timeout` param (line 17 `timeout: int = 30` is fine — the `None` case is `timeout: Optional[int] = 30` only if you need to pass None; check actual errors):

  Run first to see the exact lines:
  ```bash
  mypy opennms_api_wrapper/_base.py 2>&1 | grep "error:"
  ```

  For each `params: dict = None`, change to `params: Optional[dict[str, Any]] = None`.

- [ ] **Verify _base.py is clean**

  ```bash
  mypy opennms_api_wrapper/_base.py
  ```
  Expected: `Success: no issues found in 1 source file`

- [ ] **Commit**

  ```bash
  git add pyproject.toml opennms_api_wrapper/_base.py
  git commit -m "fix(types): add types-requests dev dep and fix _base.py Optional params"
  ```

---

## Task 2: Mixin batch A — alarms, acks, events, nodes (all 3 fix types)

These files need the mixin inheritance fix **plus** `Optional` annotations **plus** `dict[str, Any]` dict annotation.

**Files:** `_alarms.py`, `_acks.py`, `_events.py`, `_nodes.py`, `_outages.py`, `_notifications.py`, `_ifservices.py`

- [ ] **Check exact errors for each file**

  ```bash
  mypy opennms_api_wrapper/_alarms.py opennms_api_wrapper/_acks.py \
       opennms_api_wrapper/_events.py opennms_api_wrapper/_nodes.py \
       opennms_api_wrapper/_outages.py opennms_api_wrapper/_notifications.py \
       opennms_api_wrapper/_ifservices.py 2>&1 | grep "error:"
  ```

- [ ] **Fix `_alarms.py`**

  Add at top:
  ```python
  from typing import Any, Optional
  from ._base import _OpenNMSBase
  ```

  Change class line:
  ```python
  class AlarmsMixin(_OpenNMSBase):
  ```

  For every `params = {"limit": ..., "offset": ...}` dict literal that later gets string keys assigned, add explicit annotation:
  ```python
  params: dict[str, Any] = {"limit": limit, "offset": offset}
  ```

  For `order_by: str = None` and `order: str = None` parameters, change to `Optional[str] = None`.

- [ ] **Fix `_acks.py`**

  Add at top:
  ```python
  from typing import Any, Optional
  from ._base import _OpenNMSBase
  ```
  Change class: `class AcksMixin(_OpenNMSBase):`

  In `create_ack`, `alarm_id: int = None` → `alarm_id: Optional[int] = None`, same for `notification_id`.

  `data = {"action": action}` → `data: dict[str, Any] = {"action": action}`

- [ ] **Fix `_events.py`**

  Add at top:
  ```python
  from typing import Any, Optional
  from ._base import _OpenNMSBase
  ```
  Change class: `class EventsMixin(_OpenNMSBase):`

  Find the `params = {"limit": ..., "offset": ...}` dict that later gets string keys and annotate: `params: dict[str, Any] = {...}`.

  Fix any `param: str = None` signatures with `Optional[str]`.

- [ ] **Fix `_nodes.py`**

  `_nodes.py` already imports from `.types` — add the new imports on separate lines before it:
  ```python
  from typing import Any, Optional
  from ._base import _OpenNMSBase
  from .types import Node, NodeIpInterface, NodeSnmpInterface, NodeAssetRecord, HardwareEntity, Category
  ```
  Change class: `class NodesMixin(_OpenNMSBase):`

  Find `params = {"limit": ..., "offset": ...}` dicts and annotate as `dict[str, Any]`.
  Fix `Optional` parameters as indicated by mypy.

- [ ] **Fix `_outages.py`, `_notifications.py`, `_ifservices.py`**

  Same pattern: add typing + `_OpenNMSBase` imports, update class line, annotate mixed-type dicts as `dict[str, Any]`, fix `Optional` params.

- [ ] **Verify batch A**

  ```bash
  mypy opennms_api_wrapper/_alarms.py opennms_api_wrapper/_acks.py \
       opennms_api_wrapper/_events.py opennms_api_wrapper/_nodes.py \
       opennms_api_wrapper/_outages.py opennms_api_wrapper/_notifications.py \
       opennms_api_wrapper/_ifservices.py
  ```
  Expected: `Success: no issues found in 7 source files`

- [ ] **Run tests**

  ```bash
  pytest tests/test_alarms.py tests/test_acks.py tests/test_events.py \
         tests/test_nodes.py tests/test_outages.py tests/test_notifications.py \
         tests/test_ifservices.py -v
  ```
  Expected: all PASS

- [ ] **Commit**

  ```bash
  git add opennms_api_wrapper/_alarms.py opennms_api_wrapper/_acks.py \
          opennms_api_wrapper/_events.py opennms_api_wrapper/_nodes.py \
          opennms_api_wrapper/_outages.py opennms_api_wrapper/_notifications.py \
          opennms_api_wrapper/_ifservices.py
  git commit -m "fix(types): mixin inheritance + Optional + dict[str,Any] for alarms/acks/events/nodes batch"
  ```

---

## Task 3: Mixin batch B — flows, device_config, resources, graphs, perspective_poller (mixin + Optional)

**Files:** `_flows.py`, `_device_config.py`, `_resources.py`, `_graphs.py`, `_perspective_poller.py`

These have high `no_implicit_optional` counts (24, 11, 4, 4, 4) on top of the mixin fix.

- [ ] **Check exact errors**

  ```bash
  mypy opennms_api_wrapper/_flows.py opennms_api_wrapper/_device_config.py \
       opennms_api_wrapper/_resources.py opennms_api_wrapper/_graphs.py \
       opennms_api_wrapper/_perspective_poller.py 2>&1 | grep "error:"
  ```

- [ ] **Fix each file**

  For each file, add:
  ```python
  from typing import Any, Optional
  from ._base import _OpenNMSBase
  ```
  Update the class line: `class FlowsMixin(_OpenNMSBase):` etc.

  Then for every parameter reported by mypy as `"default has type None, parameter has type X"`, change `param: X = None` to `param: Optional[X] = None`.

  `_flows.py` has 24 optional errors — `if_index: int = None` → `Optional[int]` and `exporter_node: str = None` → `Optional[str]`, repeated across many methods. Find-and-replace within the file.

  `_resources.py` has `nodes: list[Any] = None` → `Optional[list[Any]]` etc.

- [ ] **Verify batch B**

  ```bash
  mypy opennms_api_wrapper/_flows.py opennms_api_wrapper/_device_config.py \
       opennms_api_wrapper/_resources.py opennms_api_wrapper/_graphs.py \
       opennms_api_wrapper/_perspective_poller.py
  ```
  Expected: `Success: no issues found in 5 source files`

- [ ] **Run tests**

  ```bash
  pytest tests/test_flows.py tests/test_device_config.py tests/test_resources.py \
         tests/test_graphs.py tests/test_perspective_poller.py -v
  ```
  Expected: all PASS

- [ ] **Commit**

  ```bash
  git add opennms_api_wrapper/_flows.py opennms_api_wrapper/_device_config.py \
          opennms_api_wrapper/_resources.py opennms_api_wrapper/_graphs.py \
          opennms_api_wrapper/_perspective_poller.py
  git commit -m "fix(types): mixin inheritance + Optional for flows/device_config/resources/graphs batch"
  ```

---

## Task 4: Mixin batch C — situations, eventconf, alarm_history, snmp/ip interfaces, feedback, measurements, health, classifications, alarm_stats (mixin + Optional)

**Files:** `_situations.py`, `_eventconf.py`, `_alarm_history.py`, `_snmpinterfaces_v2.py`, `_snmp_config.py`, `_situation_feedback.py`, `_measurements.py`, `_ipinterfaces_v2.py`, `_ifservices.py` (already done in Task 2), `_health.py`, `_classifications.py`, `_alarm_stats.py`

- [ ] **Check exact errors**

  ```bash
  mypy opennms_api_wrapper/_situations.py opennms_api_wrapper/_eventconf.py \
       opennms_api_wrapper/_alarm_history.py opennms_api_wrapper/_snmpinterfaces_v2.py \
       opennms_api_wrapper/_snmp_config.py opennms_api_wrapper/_situation_feedback.py \
       opennms_api_wrapper/_measurements.py opennms_api_wrapper/_ipinterfaces_v2.py \
       opennms_api_wrapper/_health.py opennms_api_wrapper/_classifications.py \
       opennms_api_wrapper/_alarm_stats.py 2>&1 | grep "error:"
  ```

- [ ] **Fix each file** using the shared pattern

  Add to each file:
  ```python
  from typing import Any, Optional
  from ._base import _OpenNMSBase
  ```
  Update class line to inherit from `_OpenNMSBase`.
  Fix `param: str = None` → `param: Optional[str] = None` as flagged by mypy.

  `_situations.py` has 3 optional params: `description`, `diagnostic_text`, `feedback` — all `str = None` → `Optional[str] = None`.
  `_snmpinterfaces_v2.py` has `fiql: str = None` → `Optional[str]`.
  `_situation_feedback.py` has `prefix: str = None` → `Optional[str]`.

- [ ] **Verify batch C**

  ```bash
  mypy opennms_api_wrapper/_situations.py opennms_api_wrapper/_eventconf.py \
       opennms_api_wrapper/_alarm_history.py opennms_api_wrapper/_snmpinterfaces_v2.py \
       opennms_api_wrapper/_snmp_config.py opennms_api_wrapper/_situation_feedback.py \
       opennms_api_wrapper/_measurements.py opennms_api_wrapper/_ipinterfaces_v2.py \
       opennms_api_wrapper/_health.py opennms_api_wrapper/_classifications.py \
       opennms_api_wrapper/_alarm_stats.py
  ```
  Expected: `Success: no issues found in 11 source files`

- [ ] **Run tests**

  ```bash
  pytest tests/test_situations.py tests/test_alarm_history.py \
         tests/test_alarm_stats.py tests/test_classifications.py \
         tests/test_health.py -v
  ```
  Expected: all PASS

- [ ] **Commit**

  ```bash
  git add opennms_api_wrapper/_situations.py opennms_api_wrapper/_eventconf.py \
          opennms_api_wrapper/_alarm_history.py opennms_api_wrapper/_snmpinterfaces_v2.py \
          opennms_api_wrapper/_snmp_config.py opennms_api_wrapper/_situation_feedback.py \
          opennms_api_wrapper/_measurements.py opennms_api_wrapper/_ipinterfaces_v2.py \
          opennms_api_wrapper/_health.py opennms_api_wrapper/_classifications.py \
          opennms_api_wrapper/_alarm_stats.py
  git commit -m "fix(types): mixin inheritance + Optional for situations/eventconf/snmp/measurements batch"
  ```

---

## Task 5: Mixin batch D — mixin-only files (no Optional errors, just inheritance)

The remaining 31 mixin files need only the inheritance fix (no Optional or dict annotation issues).

**Files:**
`_applications.py`, `_availability.py`, `_business_services.py`, `_categories.py`,
`_config_mgmt.py`, `_device_config.py` (if not done in batch B), `_discovery.py`,
`_email_nbi.py`, `_enlinkd.py`, `_foreign_sources.py`, `_foreign_sources_config.py`,
`_groups.py`, `_heatmap.py`, `_info.py` (check — may not have attr-defined errors),
`_javamail_config.py`, `_ksc_reports.py`, `_maps.py`, `_metadata.py`,
`_minions.py`, `_monitoring_locations.py`, `_monitoring_systems.py`,
`_provisiond.py`, `_requisition_names.py`, `_requisitions.py`,
`_resources.py` (if not done in batch B), `_sched_outages.py`, `_scv.py`,
`_situation_feedback.py` (if not done in batch C), `_situations.py` (if not done),
`_snmp_metadata.py`, `_snmptrap_nbi.py`, `_syslog_nbi.py`,
`_user_defined_links.py`, `_users.py`, `_whoami.py`

> Note: Cross-check against the attr-defined list. Files not in that list (e.g. `_pagination.py`, `_exceptions.py`) need no changes.

- [ ] **Verify which files still need the fix**

  ```bash
  source .venv/bin/activate
  mypy opennms_api_wrapper/ 2>&1 | grep "attr-defined" | sed 's|opennms_api_wrapper/||' | sed 's/:[0-9]*.*//' | sort -u
  ```

- [ ] **Apply the mixin inheritance pattern to each remaining file**

  For files without any existing imports:
  ```python
  """Original module docstring."""
  from ._base import _OpenNMSBase      # ADD THIS LINE


  class FooMixin(_OpenNMSBase):        # ADD _OpenNMSBase
  ```

  For files that already import from `.types`:
  ```python
  """Original module docstring."""
  from ._base import _OpenNMSBase      # ADD BEFORE existing imports
  from .types import SomeType          # existing — keep as-is


  class FooMixin(_OpenNMSBase):        # ADD _OpenNMSBase
  ```

- [ ] **Verify all batch D files**

  ```bash
  mypy opennms_api_wrapper/ 2>&1 | grep "attr-defined" | wc -l
  ```
  Expected: `0`

- [ ] **Run full test suite**

  ```bash
  pytest tests/ -v
  ```
  Expected: 490 passed

- [ ] **Commit**

  ```bash
  git add opennms_api_wrapper/
  git commit -m "fix(types): mixin inheritance for remaining batch D files"
  ```

---

## Task 6: Final verification and PR

- [ ] **Run full mypy check**

  ```bash
  mypy opennms_api_wrapper/
  ```
  Expected: `Success: no issues found in N source files`

- [ ] **Run full test suite**

  ```bash
  pytest tests/ -v
  ```
  Expected: 490 passed, 0 failed

- [ ] **Run ruff**

  ```bash
  ruff check opennms_api_wrapper/
  ```
  Expected: `All checks passed!`

- [ ] **Open PR**

  ```bash
  git push -u origin fix/mypy-clean
  gh pr create \
    --title "fix(types): resolve all mypy errors across mixin package" \
    --body "Fixes 427 pre-existing mypy errors across 50 files. Four change types: mixin inheritance (_OpenNMSBase base), Optional annotations, dict[str,Any] dict literals, types-requests dev dep. All 490 tests pass."
  ```
