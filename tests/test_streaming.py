import io
import json
import unittest

from geojson_utils import feature_collection_from_iter, iter_features, read_ndjson_features, write_ndjson_features


FEATURE = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [1, 2]},
    "properties": {"name": "A"},
}


class StreamingTest(unittest.TestCase):
    def test_iter_features_supports_feature_collection(self):
        collection = {"type": "FeatureCollection", "features": [FEATURE]}

        self.assertEqual(list(iter_features(collection)), [FEATURE])

    def test_read_ndjson_features(self):
        source = io.StringIO(json.dumps(FEATURE) + "\n")

        self.assertEqual(list(read_ndjson_features(source)), [FEATURE])

    def test_write_ndjson_features(self):
        target = io.StringIO()

        write_ndjson_features([FEATURE], target)

        self.assertEqual(json.loads(target.getvalue()), FEATURE)

    def test_feature_collection_from_iter(self):
        self.assertEqual(feature_collection_from_iter([FEATURE]), {"type": "FeatureCollection", "features": [FEATURE]})


if __name__ == "__main__":
    unittest.main()
