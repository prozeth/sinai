"""A Rule takes data from sources, makes metrics and puts them into stores."""
from __future__ import annotations

from sinai.metrics import AGGREGATION_CLASSES
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

