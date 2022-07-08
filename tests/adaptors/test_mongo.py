import mongomock

from sinai.stores import MongoMetricStore
from sinai.sources import MongoMetricSource, MongoSource
from sinai.metrics.base import Metric
from sinai.monitors.monitor import Monitor


@mongomock.patch(servers=(("localhost", 27017),))
def test_mongo_store_save():
    # Given we have a metric and a store
    monitor = Monitor()
    ref = "A-meaningful-id"
    metric = Metric(name="simple-save", ref=ref, value=52)
    store = MongoMetricStore(monitor)
    # When we save the metric
    store.save_metric(metric),
    # Then it is in the store
    saved_object = store.collection.find_one()
    assert saved_object["ref"] == ref
    assert saved_object["value"] == 52
    assert saved_object["name"] == "simple-save"


@mongomock.patch(servers=(("localhost", 27017),))
def test_mongo_store_upsert():
    # Given we have stored metric
    class UpdatableMetric(Metric):
        name = "upsert-by-ref"
        update = ["name", "ref"]

    ref = "relevant-to-your-app"
    metric = UpdatableMetric(ref=ref, value=1)
    monitor = Monitor()
    store = MongoMetricStore(monitor)
    store.save_metric(metric)

    # When we update the metric
    updated_metric = UpdatableMetric(ref=ref, value=2)
    store.save_metric(updated_metric)

    # Then there must only be one document
    assert store.collection.count_documents({}) == 1
    # The document is the updated metric
    saved_object = store.collection.find_one()
    assert saved_object["ref"] == ref
    assert saved_object["value"] == 2


@mongomock.patch(servers=(("localhost", 27017),))
def test_mongo_source_find_one():
    # Given we have stored data
    monitor = Monitor()
    store = MongoMetricSource(monitor)
    store.db["animals"].insert_one(
        {
            "name": "mule",
            "ears": "long funny",
            "back": "brawny",
            "brain": "weak",
            "howto": "don't go to school",
        }
    )
    # When we use the find_one method
    document = store.find_one("animals", {"name": "mule"})
    # Then we find one
    assert document["back"] == "brawny"


@mongomock.patch(servers=(("localhost", 27017),))
def test_mongo_source_find():
    # Given we have stored data
    monitor = Monitor()
    store = MongoMetricSource(monitor)
    store.db["animals"].insert_many(
        [
            {
                "name": "pig",
                "face": "dirty",
                "shoes": "terrible disgrace",
                "manner": "rude",
                "howto": "don't care a feather or a fig",
            },
            {
                "name": "fish",
                "literate": False,
                "look": "slippery",
                "caught": True,
                "howto": "if that is the sort of life is what you wish",
            },
        ]
    )
    # When we use the find method
    documents = store.find("animals", {"name": "fish"})
    # Then we find one
    docs = list(documents)
    assert len(docs) == 1
    assert docs[0]["look"] == "slippery"


@mongomock.patch(servers=(("localhost", 27017),))
def test_mongo_metric_source_get():
    # Given we have data in the store
    monitor = Monitor()

    class DrinkMetric(Metric):
        name = "swallowable_liquids"
        context = "UK"

    red_label = DrinkMetric(ref="breakfast-tea", value=2)
    bovril = DrinkMetric(ref="beef-tea", value=4)

    store = MongoMetricStore(monitor)
    store.save_metric(red_label)
    store.save_metric(bovril)

    source = MongoMetricSource(monitor)

    # When we get everything, then we get two results
    len(source.get()) == 2

    # When we get by metric name, then we get two results
    len(source.get(name="swallowable_liquids")) == 2

    # When we get by ref, then we get one result
    len(source.get(ref="beef-tea")) == 1

    # When we get by value, then we get one result
    len(source.get(value=2)) == 1

    # When we get by context, then we get two results
    len(source.get(context="UK")) == 2

    # When we get by monitor_id, then we get two results
    len(source.get(monitor_id=monitor.id)) == 2

    # When we get by a combination of fields, then we get two results
    len(source.get(monitor_id=monitor.id, context="UK")) == 2
