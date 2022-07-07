from sinai.models.monitor import Monitor
from sinai.models.rule import Rule
from sinai.models.store import Store


def test_base_rule():
    class TestMonitor(Monitor):
        stores = [Store]

    monitor = TestMonitor()
    rule = Rule(monitor)
    rule.evaluate()
