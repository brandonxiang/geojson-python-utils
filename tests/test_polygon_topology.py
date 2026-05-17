import unittest

from geojson_utils import area, centroid, close_ring, point_in_polygon, ring_is_clockwise


class PolygonTopologyTest(unittest.TestCase):
    def test_point_in_polygon_respects_holes(self):
        polygon = {
            "type": "Polygon",
            "coordinates": [
                [[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]],
                [[2, 2], [2, 8], [8, 8], [8, 2], [2, 2]],
            ],
        }

        self.assertTrue(point_in_polygon({"type": "Point", "coordinates": [1, 1]}, polygon))
        self.assertFalse(point_in_polygon({"type": "Point", "coordinates": [5, 5]}, polygon))

    def test_area_subtracts_holes(self):
        polygon = {
            "type": "Polygon",
            "coordinates": [
                [[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]],
                [[2, 2], [2, 8], [8, 8], [8, 2], [2, 2]],
            ],
        }

        self.assertEqual(area(polygon), 64)

    def test_centroid_accounts_for_holes(self):
        polygon = {
            "type": "Polygon",
            "coordinates": [
                [[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]],
                [[6, 6], [6, 8], [8, 8], [8, 6], [6, 6]],
            ],
        }

        result = centroid(polygon)

        self.assertLess(result["coordinates"][0], 5)
        self.assertLess(result["coordinates"][1], 5)

    def test_ring_orientation_helpers(self):
        ring = close_ring([[0, 0], [1, 0], [1, 1]])

        self.assertEqual(ring[0], ring[-1])
        self.assertFalse(ring_is_clockwise(ring))


if __name__ == "__main__":
    unittest.main()
