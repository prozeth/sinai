"""Support for using Mongo Databases as a source or store for data."""

from __future__ import annotations

import pymongo

from sinai.exceptions import MetricNotFound
from sinai.models.metric import Metric
from sinai.models.source import MetricSource, Source
from sinai.models.store import Store
from sinai.types import (
    FList,
    JDict,
    JDictOrNone,
    MetricId,
    MetricInstance,
    MetricList,
    MetricResult,
    MongoResult,
    MonitorInstance,
)


class MongoConnection:
    """A connection to MongoDB."""

    connection_string = ""
    database_name = ""

    def __init__(self, monitor: MonitorInstance) -> None:
        self.monitor = monitor
        self.client = pymongo.MongoClient(self.connection_string)  # type: ignore
        self.db = self.client[self.database_name]
        self.collection = self.db["metrics"]


class MongoStore(MongoConnection, Store):
    """Metric store using MongoDB. Don't forget to set `database_name` and `connection_string`."""

    def _save(self, metric: MetricInstance) -> None:
        self.collection.insert_one(metric.pre_save(self.monitor.id))

    def _find_metric_by_filter(
        self, metric: MetricInstance, metric_filter: JDict
    ) -> MetricResult:
        if result := self.collection.find_one(metric_filter):
            mongo_id = result.pop("_id")
            existing_metric = Metric.from_dict(result)
            metric.created_at = existing_metric.created_at
            return metric, mongo_id
        raise MetricNotFound(f"Metric with fields: {metric_filter} not found.")

    def _replace(self, metric: MetricInstance, metric_id: MetricId) -> None:
        self.collection.replace_one(
            {"_id": metric_id}, metric.pre_save(self.monitor.id)
        )


class MongoSource(MongoConnection, Source):
    """Gets arbitrary documents from MongoDB."""

    def find_one(
        self,
        collection: str,
        mongo_filter: JDictOrNone = None,
        *args: FList,
        **kwargs: JDict,
    ) -> MongoResult:
        """Find a single document from MongoFB."""
        return self.db[collection].find_one(mongo_filter, *args, **kwargs)

    def find(
        self,
        collection: str,
        mongo_filter: JDictOrNone = None,
        *args: FList,
        **kwargs: JDict,
    ) -> MongoResult:
        """Find documents from MongoFB."""
        return self.db[collection].find(mongo_filter, *args, **kwargs)


class MongoMetricSource(MongoSource, MetricSource):
    """Gets metrics from MongoDB."""

    def _execute_query(self, metric_filter: JDict) -> MetricList:
        return [
            self._document_to_metric(document)
            for document in self.collection.find(metric_filter)
        ]

    @staticmethod
    def _document_to_metric(document: JDict) -> MetricInstance:
        del document["_id"]
        return Metric.from_dict(document)
