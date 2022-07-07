from sinai.models.metric import Metric
from sinai.models.monitor import Monitor
from sinai.models.rule import Rule
from sinai.models.source import MetricSource, Source
from sinai.models.store import Store
from sinai.types import Evaluation


def test_base_metric_source():
    class TestRule(Rule):
        sources = [Source]
        stores = [Store]

        def evaluate(self) -> Evaluation:
            metric = Metric(
                ref="fun_id_100",
                value=1,
            )
            another = Metric(
                ref="fun_id_100",
                value=2,
            )
            return [metric, another]

    class TestMonitor(Monitor):
        rules = [TestRule]

    monitor = TestMonitor()
    monitor.execute()
    source = MetricSource(monitor)
    found_metrics = source.get(ref="fun_id_100")
    first = found_metrics[0]
    assert first.value == 1
