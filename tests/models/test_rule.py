from sinai.monitors.monitor import Monitor
from sinai.rules.base import Rule
from sinai.stores import MemoryMetricStore


def test_base_rule():
    class TestMonitor(Monitor):
        stores = [MemoryMetricStore]

    monitor = TestMonitor()
    rule = Rule(monitor)
    rule.evaluate()
