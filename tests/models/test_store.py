from sinai.metrics import Metric
from sinai.monitors.monitor import Monitor
from sinai.stores import MemoryMetricStore


def test_store():
    # Given we have stored metric
    monitor = Monitor()
    store = MemoryMetricStore(monitor)
    store.clear()
    assert len(store.memory) == 0
    ref = "some-relevant-id-in-your-system"
    metric = Metric(ref=ref, value=1)
    store.save_metric(metric),
    # Then it is in the store
    assert len(store.memory) == 1
    metric_tuples = list(store.memory.items())
    saved_object = metric_tuples[0][1]
    assert saved_object["ref"] == ref
    assert saved_object["value"] == 1


def test_store_update():
    # Given we have a stored metric
    monitor = Monitor()
    store = MemoryMetricStore(monitor)
    store.clear()
    assert len(store.memory) == 0

    class UpdatableMetric(Metric):
        name = "upsert-by-name-ref"
        update = ["name", "ref"]

    ref = "useful-to-your-app"

    metric = UpdatableMetric(ref=ref, value=1)
    store.save_metric(metric)
    assert len(store.memory) == 1

    # When we update the metric
    updated_metric = UpdatableMetric(ref=ref, value=2)
    store.save_metric(updated_metric)

    # Then there must only be one document
    assert len(store.memory) == 1
    # The document is the updated metric
    metric_tuples = list(store.memory.items())
    saved_object = metric_tuples[0][1]
    assert saved_object["ref"] == ref
    assert saved_object["value"] == 2
