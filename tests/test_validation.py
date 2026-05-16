import unittest

from geojson_utils import GeoJSONValidationError, normalize_geojson, validate_geojson


class ValidationTest(unittest.TestCase):
    def test_validates_all_geometry_types(self):
        geometries = [
            {"type": "Point", "coordinates": [1, 2]},
            {"type": "MultiPoint", "coordinates": [[1, 2], [3, 4]]},
            {"type": "LineString", "coordinates": [[1, 2], [3, 4]]},
            {"type": "MultiLineString", "coordinates": [[[1, 2], [3, 4]]]},
            {"type": "Polygon", "coordinates": [[[0, 0], [4, 0], [4, 4], [0, 0]]]},
            {"type": "MultiPolygon", "coordinates": [[[[0, 0], [4, 0], [4, 4], [0, 0]]]]},
            {
                "type": "GeometryCollection",
                "geometries": [{"type": "Point", "coordinates": [1, 2]}],
            },
        ]

        for geometry in geometries:
            self.assertIs(validate_geojson(geometry), geometry)

    def test_validates_feature_collection(self):
        collection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [1, 2]},
                    "properties": {"name": "A"},
                }
            ],
        }

        self.assertIs(validate_geojson(collection), collection)

    def test_invalid_geojson_has_clear_error(self):
        with self.assertRaisesRegex(GeoJSONValidationError, r"\$\.coordinates: missing coordinates"):
            validate_geojson({"type": "Point"})

    def test_polygon_ring_must_be_closed(self):
        with self.assertRaisesRegex(GeoJSONValidationError, "linear ring must be closed"):
            validate_geojson({"type": "Polygon", "coordinates": [[[0, 0], [4, 0], [4, 4], [0, 4]]]})

    def test_normalize_closes_polygon_rings_and_strips_metadata(self):
        source = {
            "type": "Polygon",
            "bbox": [0, 0, 4, 4],
            "coordinates": [[[0, 0], [4, 0], [4, 4], [0, 4]]],
        }

        result = normalize_geojson(source, keep_bbox=False)

        self.assertNotIn("bbox", result)
        self.assertEqual(result["coordinates"][0][0], result["coordinates"][0][-1])
        self.assertNotEqual(source["coordinates"][0][0], source["coordinates"][0][-1])

    def test_normalize_orients_holes_clockwise(self):
        polygon = {
            "type": "Polygon",
            "coordinates": [
                [[0, 0], [4, 0], [4, 4], [0, 0]],
                [[1, 1], [1, 2], [2, 1], [1, 1]],
            ],
        }

        result = normalize_geojson(polygon, orient_rings=True)

        self.assertEqual(result["coordinates"][0], [[0, 0], [4, 0], [4, 4], [0, 0]])
        self.assertEqual(result["coordinates"][1], [[1, 1], [1, 2], [2, 1], [1, 1]])


if __name__ == "__main__":
    unittest.main()
