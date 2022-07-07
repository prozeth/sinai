"""Monitor cat facts."""
from sinai.adaptors.api import ApiSource
from sinai.adaptors.mongo import MongoMetricSource, MongoStore
from sinai.models.metric import Metric
from sinai.models.monitor import Monitor
from sinai.models.rule import MetricAggregationRule, Rule


class CatMongoMetricSource(MongoMetricSource):
    connection_string = "mongodb://localhost:27017/"
    database_name = "metrics"


class CatMongoMetricStore(MongoStore):
    connection_string = "mongodb://localhost:27017/"
    database_name = "metrics"


class CatFactSource(ApiSource):
    url = "https://catfact.ninja/fact"


class CatFactMetric(Metric):
    name = "cat_fact"


class CatFactRule(Rule):
    """Record the cat fact."""

    sources = [CatFactSource]
    stores = [CatMongoMetricStore]

    def evaluate(self):
        cat_fact = self.monitor.source(CatFactSource)
        metric = CatFactMetric(value=cat_fact.content["length"])
        metric.annotate(cat_fact.content["fact"])
        return metric


class CatRecordMetric(Metric):
    name = "cat_fact_record"


class MaxLengthRule(MetricAggregationRule):
    """Record the longest fact length we have seen."""

    sources = [CatMongoMetricSource]
    stores = [CatMongoMetricStore]
    max = [CatFactMetric]
    update = ["name"]


class FactCountRule(MetricAggregationRule):
    """Record the number of facts we have seen."""

    sources = [CatMongoMetricSource]
    stores = [CatMongoMetricStore]
    count = [CatFactMetric]
    update = ["name"]


class TotalLengthRule(MetricAggregationRule):
    """Record the total length of facts we have seen."""

    sources = [CatMongoMetricSource]
    stores = [CatMongoMetricStore]
    sum = [CatFactMetric]
    update = ["name"]


class CatMonitor(Monitor):
    rules = [CatFactRule, MaxLengthRule, FactCountRule, TotalLengthRule]


if __name__ == "__main__":
    cat_monitor = CatMonitor()
    cat_monitor.execute()
    print("Done.")
