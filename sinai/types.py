"""Custom Data Types for Sinai."""

from decimal import Decimal
from numbers import Number
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Sequence,
    Set,
    Tuple,
    Type,
    Union,
)
from uuid import UUID

from typing_extensions import TypeAlias

if TYPE_CHECKING:  # pragma: no cover
    from sinai.models.metric import AggregationMetric, Metric  # noqa: F401
    from sinai.models.monitor import Monitor  # noqa: F401
    from sinai.models.rule import Rule
    from sinai.models.source import MetricSource, Source  # noqa: F401
    from sinai.models.store import Store

    try:
        from bson.objectid import ObjectId  # pylint: disable=W0611
    except ImportError:
        pass


# Common Data Types
JDict = Dict[str, Any]  # A JSON-Safe Dictionary
JDictOrNone = Union[JDict, None]  # A JSON-Safe Dictionary or none
FList = List[Any]  # A Freeform List
SList = List[str]  # A List of Strings

# Metric types
MetricInstance: TypeAlias = "Metric"
MetricList = List[MetricInstance]
MetricClass = Type[MetricInstance]
MetricClasses = List[MetricClass]
MetricId = Union[UUID, "ObjectId", str]
MetricDict = Dict[MetricId, MetricInstance]
MetricResult = Tuple[MetricInstance, MetricId]
MetricValue = Union[Number, Decimal, None, int, float]
MetricValueList = List[MetricValue]
AggregationFunction = Callable[[MetricValueList], MetricValue]
AggregationMetrics = List["AggregationMetric"]
Evaluation = Union[List[MetricInstance], AggregationMetrics, MetricInstance, None]

# Monitor Types
MonitorInstance: TypeAlias = "Monitor"
GlobalMemory = Dict[MetricId, JDict]

# Rule types
RuleClass = Type["Rule"]
RuleClasses = List[RuleClass]

# Store types
StoreClass = Type["Store"]
StoreClassSet = Set[StoreClass]
StoreDict = Dict[StoreClass, "Store"]
StoreClasses = Sequence[StoreClass]

# Source types
SourceInstance: TypeAlias = "Source"
SourceClass = Type[SourceInstance]
SourceClassSet = Set[SourceClass]
SourceDict = Dict[SourceClass, SourceInstance]
SourceClasses = Sequence[SourceClass]

# MetricSource types
MetricSourceInstance: TypeAlias = "MetricSource"
MetricSourceClass = Type[MetricSourceInstance]
MetricSourceClasses = Sequence[MetricSourceClass]


# ApiSource types
RequestHeader = Dict[str, str]

# Mongo adapter types
MongoResult: TypeAlias = Any
