from sinai.metrics.base import Metric
from sinai.monitors.monitor import Monitor
from sinai.rules.base import Rule
from sinai.sources.base import MetricSource, Source
from sinai.stores import MemoryMetricStore
from sinai.types import Evaluation


class ExampleRule(Rule):
    sources = [MetricSource]
    stores = [MemoryMetricStore]

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


class ExampleMonitor(Monitor):
    rules = [ExampleRule]


def test_base_metric_source():
    monitor = ExampleMonitor()
    monitor.execute()
    source = monitor.source(MetricSource)
    assert len(source.memory) == 2
    found_metrics = source.get(ref="fun_id_100")
    first = found_metrics[0]
    assert first.value == 1
