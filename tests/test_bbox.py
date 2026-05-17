import unittest

from geojson_utils import BBoxIndex, bbox, filter_features_by_bbox, intersects_bbox


class BBoxTest(unittest.TestCase):
    def test_bbox_for_feature_collection(self):
        collection = {
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [1, 2]}, "properties": {}},
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [3, 4]}, "properties": {}},
            ],
        }

        self.assertEqual(bbox(collection), [1, 2, 3, 4])

    def test_intersects_bbox_includes_edges(self):
        self.assertTrue(intersects_bbox([0, 0, 1, 1], [1, 1, 2, 2]))
        self.assertFalse(intersects_bbox([0, 0, 1, 1], [2, 2, 3, 3]))

    def test_filter_features_by_bbox(self):
        collection = {
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [1, 2]}, "properties": {"id": 1}},
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [10, 20]}, "properties": {"id": 2}},
            ],
        }

        result = filter_features_by_bbox(collection, [0, 0, 5, 5])

        self.assertEqual(len(result["features"]), 1)
        self.assertEqual(result["features"][0]["properties"]["id"], 1)

    def test_bbox_index_search(self):
        collection = {
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [1, 2]}, "properties": {"id": 1}},
                {"type": "Feature", "geometry": {"type": "Point", "coordinates": [10, 20]}, "properties": {"id": 2}},
            ],
        }

        result = BBoxIndex(collection).search([9, 19, 11, 21])

        self.assertEqual(result["features"][0]["properties"]["id"], 2)


if __name__ == "__main__":
    unittest.main()
