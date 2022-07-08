"""A Metric is the output of a rule, and often the input to rules too.
Metrics can be stored in a Store, and can be retrieved by a MetricSource."""
import datetime
from uuid import uuid4

from sinai.types import JDict, MetricValue, SList


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
