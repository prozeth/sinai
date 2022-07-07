from sinai.models.monitor import Monitor
from sinai.models.rule import Rule
from sinai.models.store import Store


def test_monitor():
    class TestMonitor(Monitor):
        rules = [Rule]
        sources = []
        stores = [Store]
