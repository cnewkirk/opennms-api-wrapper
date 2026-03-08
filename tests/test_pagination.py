"""Tests for client.paginate()."""
import json

import pytest
import responses as rsps

import opennms_api_wrapper as opennms
from tests.conftest import V1


def alarm_page(items, total):
    """Build an alarm list response page."""
    return {"alarm": items, "totalCount": total, "count": len(items), "offset": 0}


def node_page(items, total):
    """Build a node list response page."""
    return {"node": items, "totalCount": total, "count": len(items), "offset": 0}


def _alarm(id_):
    return {"id": id_, "severity": "MAJOR"}


def _node(id_):
    return {"id": id_, "label": f"node-{id_}"}


ALARMS_URL = f"{V1}/alarms"
NODES_URL = f"{V1}/nodes"


# ---------------------------------------------------------------------------
# Basic behaviour
# ---------------------------------------------------------------------------

@rsps.activate
def test_single_page_under_page_size(client):
    """Fewer items than page_size → one request, all items yielded."""
    rsps.add(rsps.GET, ALARMS_URL,
             body=json.dumps(alarm_page([_alarm(1), _alarm(2)], total=2)),
             content_type="application/json")
    result = list(client.paginate(client.get_alarms, "alarm"))
    assert result == [_alarm(1), _alarm(2)]
    assert len(rsps.calls) == 1


@rsps.activate
def test_exact_page_size_stops_at_total_count(client):
    """Items == page_size but offset == totalCount → stops after one request."""
    rsps.add(rsps.GET, ALARMS_URL,
             body=json.dumps(alarm_page([_alarm(i) for i in range(3)], total=3)),
             content_type="application/json")
    result = list(client.paginate(client.get_alarms, "alarm", page_size=3))
    assert len(result) == 3
    assert len(rsps.calls) == 1


@rsps.activate
def test_exact_page_size_no_total_count(client):
    """Items == page_size with no totalCount → fetches next page to confirm end."""
    page1 = [_alarm(i) for i in range(3)]
    rsps.add(rsps.GET, ALARMS_URL,
             body=json.dumps({"alarm": page1, "count": 3}),
             content_type="application/json")
    rsps.add(rsps.GET, ALARMS_URL,
             body=json.dumps({"alarm": [], "count": 0}),
             content_type="application/json")
    result = list(client.paginate(client.get_alarms, "alarm", page_size=3))
    assert len(result) == 3
    assert len(rsps.calls) == 2


@rsps.activate
def test_multiple_full_pages(client):
    """Two full pages + partial third page returns all items."""
    page1 = [_alarm(i) for i in range(1, 4)]
    page2 = [_alarm(i) for i in range(4, 7)]
    page3 = [_alarm(7)]
    rsps.add(rsps.GET, ALARMS_URL,
             body=json.dumps(alarm_page(page1, total=7)),
             content_type="application/json")
    rsps.add(rsps.GET, ALARMS_URL,
             body=json.dumps(alarm_page(page2, total=7)),
             content_type="application/json")
    rsps.add(rsps.GET, ALARMS_URL,
             body=json.dumps(alarm_page(page3, total=7)),
             content_type="application/json")
    result = list(client.paginate(client.get_alarms, "alarm", page_size=3))
    assert len(result) == 7
    assert result[0] == _alarm(1)
    assert result[-1] == _alarm(7)
    assert len(rsps.calls) == 3


@rsps.activate
def test_stops_at_total_count(client):
    """Stops when offset reaches totalCount even with a full page returned."""
    items = [_alarm(i) for i in range(1, 4)]
    rsps.add(rsps.GET, ALARMS_URL,
             body=json.dumps(alarm_page(items, total=3)),
             content_type="application/json")
    result = list(client.paginate(client.get_alarms, "alarm", page_size=3))
    assert len(result) == 3
    assert len(rsps.calls) == 1


@rsps.activate
def test_empty_result_set(client):
    """Zero items returns empty list, makes exactly one request."""
    rsps.add(rsps.GET, ALARMS_URL,
             body=json.dumps(alarm_page([], total=0)),
             content_type="application/json")
    result = list(client.paginate(client.get_alarms, "alarm"))
    assert result == []
    assert len(rsps.calls) == 1


# ---------------------------------------------------------------------------
# kwargs forwarding
# ---------------------------------------------------------------------------

@rsps.activate
def test_kwargs_forwarded_to_method(client):
    """Extra kwargs are passed through to the underlying method."""
    rsps.add(rsps.GET, ALARMS_URL,
             body=json.dumps(alarm_page([_alarm(1)], total=1)),
             content_type="application/json")
    list(client.paginate(client.get_alarms, "alarm",
                         severity="MAJOR", order_by="lastEventTime"))
    qs = rsps.calls[0].request.url
    assert "severity=MAJOR" in qs
    assert "orderBy=lastEventTime" in qs


# ---------------------------------------------------------------------------
# page_size default
# ---------------------------------------------------------------------------

@rsps.activate
def test_default_page_size_is_100(client):
    """Default page_size sends limit=100."""
    rsps.add(rsps.GET, ALARMS_URL,
             body=json.dumps(alarm_page([], total=0)),
             content_type="application/json")
    list(client.paginate(client.get_alarms, "alarm"))
    assert "limit=100" in rsps.calls[0].request.url


@rsps.activate
def test_custom_page_size(client):
    """Custom page_size is forwarded as limit."""
    rsps.add(rsps.GET, ALARMS_URL,
             body=json.dumps(alarm_page([], total=0)),
             content_type="application/json")
    list(client.paginate(client.get_alarms, "alarm", page_size=25))
    assert "limit=25" in rsps.calls[0].request.url


# ---------------------------------------------------------------------------
# Works with different endpoints
# ---------------------------------------------------------------------------

@rsps.activate
def test_works_with_nodes(client):
    """paginate works with the nodes endpoint and 'node' key."""
    rsps.add(rsps.GET, NODES_URL,
             body=json.dumps(node_page([_node(1), _node(2)], total=2)),
             content_type="application/json")
    result = list(client.paginate(client.get_nodes, "node"))
    assert len(result) == 2
    assert result[0] == _node(1)


# ---------------------------------------------------------------------------
# Generator behaviour
# ---------------------------------------------------------------------------

@rsps.activate
def test_is_generator(client):
    """paginate returns a generator (lazy evaluation)."""
    rsps.add(rsps.GET, ALARMS_URL,
             body=json.dumps(alarm_page([_alarm(1)], total=1)),
             content_type="application/json")
    import types
    gen = client.paginate(client.get_alarms, "alarm")
    assert isinstance(gen, types.GeneratorType)


@rsps.activate
def test_partial_consumption(client):
    """Stopping iteration mid-way does not fetch unnecessary pages."""
    page1 = [_alarm(i) for i in range(1, 4)]
    rsps.add(rsps.GET, ALARMS_URL,
             body=json.dumps(alarm_page(page1, total=100)),
             content_type="application/json")
    gen = client.paginate(client.get_alarms, "alarm", page_size=3)
    first = next(gen)
    assert first == _alarm(1)
    # Only one HTTP request made so far (first page fetched on first next())
    assert len(rsps.calls) == 1
