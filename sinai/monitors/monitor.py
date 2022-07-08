"""
Monitor (gets all data, evaluates commandments
stores commandment outcome and stores metrics)
    get data
    run rule
        rules generate metrics (some rules are simple, some require processing)
    store metrics
"""
from collections.abc import Iterable
from uuid import uuid4

from sinai.metrics import Metric
from sinai.rules import Rule
from sinai.types import (
    Evaluation,
    RuleClass,
    RuleClasses,
    SourceClass,
    SourceClassSet,
    SourceDict,
    SourceInstance,
    StoreClassSet,
    StoreDict,
)


class Monitor:
    """The monitor controls the monitoring run."""

    rules: RuleClasses = []

    def __init__(self) -> None:
        self.id = str(uuid4())
        self.sources: SourceClassSet = set()
        self.stores: StoreClassSet = set()
        self._store_instances: StoreDict = {}
        self._source_instances: SourceDict = {}
        self._resolve_rules()

    def _resolve_rules(self) -> None:
        for rule in self.rules:
            self.sources.update(rule.sources)
            self.stores.update(rule.stores)

    def _connect_sources(self) -> None:
        for source_class in self.sources:
            self._source_instances[source_class] = source_class(monitor=self)

    def _connect_stores(self) -> None:
        for store_class in self.stores:
            self._store_instances[store_class] = store_class(monitor=self)

    def _evaluate_rules(self) -> None:
        for rule_class in self.rules:
            self._evaluate_rule(rule_class)

    def _evaluate_rule(self, rule_class: RuleClass) -> None:
        rule = rule_class(self)
        result: Evaluation = rule.evaluate()
        if isinstance(result, Iterable):
            for metric in result:
                self.store_metric(rule, metric)
        elif not result:
            return
        else:
            self.store_metric(rule, result)

    def execute(self) -> None:
        """Start monitoring."""
        self._connect_stores()
        self._connect_sources()
        self._evaluate_rules()

    def source(self, source: SourceClass) -> SourceInstance:
        """Return an instatatied source."""
        return self._source_instances[source]

    def store_metric(self, rule: Rule, metric: Metric) -> None:
        """Store a metric."""
        for store_class in rule.stores:
            store = self._store_instances[store_class]
            store.save_metric(metric)
