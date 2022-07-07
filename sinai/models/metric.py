"""A Metric is the output of a rule, and often the input to rules too.
Metrics can be stored in a Store, and can be retrieved by a MetricSource."""
import datetime
from statistics import mean, median, mode
from uuid import uuid4

from sinai.types import AggregationFunction, JDict, MetricValue, MetricValueList, SList


class Metric:
    """A measure to be observed."""

    name: str = "monitoring_metric"
    context: str = ""
    update: SList = []

    def __init__(
        self,
        value: MetricValue = None,
        name: str = "",
        ref: str = "",
        context: str = "",
        update: SList = [],
    ) -> None:
        if name:
            self.name = name
        if context:
            self.context = context
        if update:
            self.update = update
        self.annotations: SList = []
        self.monitor_id: str = ""
        self.ref = ref or str(uuid4())
        self.value = value
        self.created_at = datetime.datetime.now(tz=datetime.timezone.utc)
        self.updated_at = self.created_at

    def pre_save(self, monitor_id: str) -> JDict:
        """Readythe Metric for storage."""
        self.updated_at = datetime.datetime.now(tz=datetime.timezone.utc)
        self.monitor_id = monitor_id
        return self.to_dict()

    def to_dict(self) -> JDict:
        """Serialise the Metric to a dictionary."""
        return {
            "name": self.name,
            "ref": self.ref,
            "value": self.value,
            "context": self.context,
            "annotations": self.annotations,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "monitor_id": self.monitor_id,
        }

    @classmethod
    def from_dict(cls, metric_dict: JDict) -> "Metric":
        """Deserialise a dictionary back to a Metric."""
        metric = cls(
            name=metric_dict["name"],
            ref=metric_dict["ref"],
            value=metric_dict["value"],
            context=metric_dict["context"],
        )
        metric.created_at = metric_dict["created_at"]
        metric.updated_at = metric_dict["updated_at"]
        metric.annotations = metric_dict["annotations"]
        metric.monitor_id = metric_dict["monitor_id"]
        return metric

    def annotate(self, text: str) -> None:
        """Store a piece of text in the Metric."""
        self.annotations.append(text)


class Sinner(Metric):
    """An unexpected or missing item between two sequences."""

    ...


class AggregationMetric(Metric):
    """A metric formed from summarizing a query of stored metrics."""

    name = "aggregation"
    aggregation: AggregationFunction = len

    def process_data_points(self, data_points: MetricValueList) -> None:
        """Turn multiple values into one."""
        self.value = self.aggregation(data_points)  # type:ignore


class CountMetric(AggregationMetric):
    """The total number of matching metrics."""

    name = "count"
    aggregation = len


class SumMetric(AggregationMetric):
    """The total values of matching metric."""

    name = "sum"
    aggregation = sum  # type:ignore


class MeanMetric(AggregationMetric):
    """The average of matching metric values."""

    name = "mean"
    aggregation = mean


class MaxMetric(AggregationMetric):
    """The maximum of the matching metric values."""

    name = "max"
    aggregation = max  # type:ignore


class MinMetric(AggregationMetric):
    """The minimum of the matching metric values."""

    name = "min"
    aggregation = min  # type:ignore


class MedianMetric(AggregationMetric):
    """The median of the matching metric values."""

    name = "median"
    aggregation = median


class ModeMetric(AggregationMetric):
    """The mode of the matching metric values."""

    name = "mode"
    aggregation = mode


AGGREGATION_CLASSES = {
    "count": CountMetric,
    "sum": SumMetric,
    "mean": MeanMetric,
    "max": MaxMetric,
    "min": MinMetric,
    "median": MedianMetric,
    "mode": ModeMetric,
}
