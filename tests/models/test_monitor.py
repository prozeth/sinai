from sinai.monitors.monitor import Monitor
from sinai.rules.base import Rule
from sinai.stores import MemoryMetricStore


def test_monitor():
    class TestMonitor(Monitor):
        rules = [Rule]
        sources = []
        stores = [MemoryMetricStore]
