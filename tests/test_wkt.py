import unittest

from geojson_utils import convert, geojson_to_wkt, wkt_to_geojson


class WKTTest(unittest.TestCase):
    def test_point_round_trip(self):
        point = {"type": "Point", "coordinates": [1, 2]}

        self.assertEqual(geojson_to_wkt(point), "POINT (1 2)")
        self.assertEqual(wkt_to_geojson("POINT (1 2)"), point)

    def test_polygon_round_trip(self):
        polygon = {"type": "Polygon", "coordinates": [[[0, 0], [4, 0], [4, 4], [0, 0]]]}

        self.assertEqual(wkt_to_geojson(geojson_to_wkt(polygon)), polygon)

    def test_geometry_collection_round_trip(self):
        collection = {
            "type": "GeometryCollection",
            "geometries": [
                {"type": "Point", "coordinates": [1, 2]},
                {"type": "LineString", "coordinates": [[1, 2], [3, 4]]},
            ],
        }

        self.assertEqual(wkt_to_geojson(geojson_to_wkt(collection)), collection)

    def test_registered_wkt_converter(self):
        point = {"type": "Point", "coordinates": [1, 2]}

        self.assertEqual(convert(point, "geojson", "wkt"), "POINT (1 2)")
        self.assertEqual(convert("POINT (1 2)", "wkt", "geojson"), point)


if __name__ == "__main__":
    unittest.main()
