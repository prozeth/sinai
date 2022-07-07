"""A Store is any output channel from a rule."""

from dataclasses import dataclass
from uuid import uuid4

from sinai.exceptions import MetricNotFound
from sinai.types import JDict, MetricId, MetricInstance, MetricResult, MonitorInstance


@dataclass
class Store:
    """Basic in memory metric store.
    This is the base class. You want to us an adaptors to get persistence."""

    def __init__(self, monitor: MonitorInstance) -> None:
        self.monitor = monitor

    def save_metric(self, metric: MetricInstance) -> None:
        """Save a metric instance into the store."""
        if metric.update:
            self._upsert(metric)
        else:
            self._save(metric)

    def _save(self, metric: MetricInstance) -> None:
        self.monitor.memory[uuid4()] = metric.pre_save(self.monitor.id)

    def _upsert(self, metric: MetricInstance) -> None:
        try:
            existing, metric_id = self._get_metric_for_update(metric)
        except MetricNotFound:
            self._save(metric)
        else:
            self._replace(existing, metric_id)

    def _replace(self, metric: MetricInstance, metric_id: MetricId) -> None:
        self.monitor.memory[metric_id] = metric.pre_save(self.monitor.id)

    def _get_metric_for_update(self, metric: MetricInstance) -> MetricResult:
        metric_filter: JDict = {}
        for field in metric.update:
            metric_filter[field] = getattr(metric, field)
        return self._find_metric_by_filter(metric, metric_filter)

    def _find_metric_by_filter(
        self, metric: MetricInstance, metric_filter: JDict
    ) -> MetricResult:
        if results := self.monitor.find_metric(metric_filter):
            for metric_id, existing_metric in results.items():
                metric.created_at = existing_metric.created_at
                # This could support updating multiple metrics, for now support only the first
                return metric, metric_id
        raise MetricNotFound(f"Metric with fields: {metric_filter} not found.")
