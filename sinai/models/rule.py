"""A Rule takes data from sources, makes metrics and puts them into stores."""
from __future__ import annotations

from sinai.models.metric import AGGREGATION_CLASSES
from sinai.types import (
    AggregationMetrics,
    Evaluation,
    MetricClasses,
    MetricList,
    MetricSourceClass,
    MetricSourceClasses,
    MetricSourceInstance,
    MonitorInstance,
    SList,
    SourceClasses,
    StoreClasses,
)


class Rule:
    """The sources and stores are defined in the rule, instantiated by the monitor."""

    sources: SourceClasses = []
    stores: StoreClasses = []

    def __init__(self, monitor: MonitorInstance):
        self.monitor = monitor

    def evaluate(self) -> Evaluation:
        """The evalutation function is called by the monitor, which stores any returned metrics."""
        return None


class Commandment(Rule):
    """a rule that compares 2 lists and finds 'sinners'"""

    ...


class MetricAggregationRule(Rule):
    """A rule that aggregates stored metrics and produces a metric."""

    sources: MetricSourceClasses = []
    update: SList = []
    count: MetricClasses = []
    sum: MetricClasses = []
    max: MetricClasses = []
    min: MetricClasses = []
    mean: MetricClasses = []
    mode: MetricClasses = []
    median: MetricClasses = []
    last_only = False

    def evaluate(self) -> Evaluation:
        self.metrics: AggregationMetrics = []
        for agg in AGGREGATION_CLASSES:
            met_cls = getattr(self, agg)
            if met_cls:
                base_name = "+".join([cls.name for cls in met_cls])
                self._process_agg(agg, base_name)
        return self.metrics

    def _process_agg(self, aggregation_name: str, base_name: str) -> None:
        metric_instances = []
        for source_cls in self.sources:
            metric_instances.extend(
                self._get_metric_instances(source_cls, aggregation_name)
            )
        data_points = [metric.value for metric in metric_instances]
        metric_cls = AGGREGATION_CLASSES[aggregation_name]
        metric = metric_cls(name=f"{base_name}:{metric_cls.name}", update=self.update)
        metric.process_data_points(data_points)
        self.metrics.append(metric)

    def _get_metric_instances(
        self, source_cls: MetricSourceClass, aggregation_name: str
    ) -> MetricList:
        metric_instances = []
        source: MetricSourceInstance = self.monitor.source(source_cls)  # type: ignore
        for target_class in getattr(self, aggregation_name):
            if self.last_only:
                instances = source.get(name=target_class.name, monitor_id=self.monitor.id)
            else:
                instances = source.get(name=target_class.name)
            metric_instances.extend(instances)
        return metric_instances
