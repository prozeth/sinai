"""A `Source` provides the input data to the Rule."""

from sinai.types import JDict, MetricList, MonitorInstance


class Source:
    """Any data source (base class)."""

    def __init__(self, monitor: MonitorInstance):
        self.monitor = monitor


class MetricSource(Source):
    """In memory source of Metrics, use an adaptor instead when you need persistence."""

    def get(
        self,
        name: str = "",
        ref: str = "",
        value: str = "",
        context: str = "",
        monitor_id: str = "",
    ) -> MetricList:
        """Get a metric/metrics from the Source"""
        metric_filter = {}
        if name:
            metric_filter["name"] = name
        if ref:
            metric_filter["ref"] = ref
        if value:
            metric_filter["value"] = value
        if context:
            metric_filter["context"] = context
        if monitor_id:
            metric_filter["monitor_id"] = monitor_id
        return self._execute_query(metric_filter)

    def _execute_query(self, metric_filter: JDict) -> MetricList:
        results = self.monitor.find_metric(metric_filter)
        return list(results.values())
