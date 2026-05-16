import unittest

from geojson_utils import convertor


class ConvertorPipelineTest(unittest.TestCase):
    def test_convertor_can_return_copy(self):
        point = {"type": "Point", "coordinates": [116.391, 39.907]}

        converted = convertor(point, method="wgs2gcj", inplace=False)

        self.assertNotEqual(converted["coordinates"], point["coordinates"])
        self.assertEqual(point["coordinates"], [116.391, 39.907])

    def test_convertor_handles_feature_collection(self):
        collection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "MultiPoint", "coordinates": [[116.391, 39.907], [121.473, 31.23]]},
                    "properties": {},
                }
            ],
        }

        converted = convertor(collection, method="wgs2gcj", inplace=False)

        self.assertNotEqual(
            converted["features"][0]["geometry"]["coordinates"],
            collection["features"][0]["geometry"]["coordinates"],
        )

    def test_convertor_handles_geometry_collection(self):
        geometry = {
            "type": "GeometryCollection",
            "geometries": [{"type": "Point", "coordinates": [116.391, 39.907]}],
        }

        converted = convertor(geometry, method="gcj2bd", inplace=False)

        self.assertNotEqual(converted["geometries"][0]["coordinates"], geometry["geometries"][0]["coordinates"])

    def test_convertor_rejects_unknown_method(self):
        with self.assertRaisesRegex(ValueError, "unsupported coordinate conversion method"):
            convertor({"type": "Point", "coordinates": [1, 2]}, method="unknown")


if __name__ == "__main__":
    unittest.main()
