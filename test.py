from __future__ import print_function
import unittest
import json
import math


class Test(unittest.TestCase):

    def test_linestrings_intersect(self):
        from geojson_utils import linestrings_intersect
        diagonal_up_str = '{ "type": "LineString","coordinates": [[0, 0], [10, 10]]}'
        diagonal_down_str = '{ "type": "LineString","coordinates": [[10, 0], [0, 10]]}'
        far_away_str = '{ "type": "LineString","coordinates": [[100, 100], [110, 110]]}'
        diagonal_up = json.loads(diagonal_up_str)
        diagonal_down = json.loads(diagonal_down_str)
        far_away = json.loads(far_away_str)
        self.assertEqual(linestrings_intersect(diagonal_up, diagonal_down), [{'type': 'Point', 'coordinates': [5, 5]}])
        self.assertEqual(linestrings_intersect(diagonal_up, far_away), [])

    def test_point_in_polygon(self):
        from geojson_utils import point_in_polygon
        in_str = '{"type": "Point", "coordinates": [5, 5]}'
        out_str = '{"type": "Point", "coordinates": [15, 15]}'
        box_str = '{"type": "Polygon","coordinates": [[ [0, 0], [10, 0], [10, 10], [0, 10] ]]}'
        in_box = json.loads(in_str)
        out_box = json.loads(out_str)
        box = json.loads(box_str)
        self.assertTrue(point_in_polygon(in_box, box))
        self.assertFalse(point_in_polygon(out_box, box))

    def test_point_in_multipolygon(self):
        from geojson_utils import point_in_multipolygon
        point_str = '{"type": "Point", "coordinates": [0.5, 0.5]}'
        single_point_str = '{"type": "Point", "coordinates": [-1, -1]}'
        multipoly_str = '{"type":"MultiPolygon","coordinates":[[[[0,0],[0,10],[10,10],[10,0],[0,0]]],[[[10,10],[10,20],[20,20],[20,10],[10,10]]]]}'
        point = json.loads(point_str)
        single_point = json.loads(single_point_str)
        multipoly = json.loads(multipoly_str)
        self.assertTrue(point_in_multipolygon(point, multipoly))
        self.assertFalse(point_in_multipolygon(single_point, multipoly))

    def test_drawCircle(self):
        from geojson_utils import draw_circle
        pt_center = json.loads('{"type": "Point", "coordinates": [0, 0]}')
        self.assertEqual(
            len(draw_circle(10, pt_center)['coordinates'][0]), 15)
        self.assertEqual(
            len(draw_circle(10, pt_center, 50)['coordinates'][0]), 50)

    def test_rectangle_centroid(self):
        from geojson_utils import rectangle_centroid
        box_str = '{"type": "Polygon","coordinates": [[[0, 0],[10, 0],[10, 10],[0, 10]]]}'
        box = json.loads(box_str)
        centroid = rectangle_centroid(box)
        self.assertEqual(centroid['coordinates'], [5, 5])

    def test_point_distance(self):
        from geojson_utils import point_distance
        fairyland_str = '{"type": "Point", "coordinates": [-122.260000705719, 37.80919060818706]}'
        navalbase_str = '{"type": "Point", "coordinates": [-122.32083320617676, 37.78774223089045]}'
        fairyland = json.loads(fairyland_str)
        navalbase = json.loads(navalbase_str)
        self.assertEqual(math.floor(
            point_distance(fairyland, navalbase)), 5852)

    def test_geometry_radius(self):
        from geojson_utils import geometry_within_radius
        center_point_str = '{"type": "Point", "coordinates":  [-122.260000705719, 37.80919060818706]}'
        check_point_str = '{"type": "Point", "coordinates": [-122.32083320617676, 37.78774223089045]}'
        center_point = json.loads(center_point_str)
        check_point = json.loads(check_point_str)
        self.assertTrue(geometry_within_radius(check_point, center_point, 5853))

    def test_area(self):
        from geojson_utils import area
        box_str = '{"type": "Polygon","coordinates": [[ [0, 0], [10, 0], [10, 10], [0, 10] ]]}'
        box = json.loads(box_str)
        self.assertEqual(area(box), 100)

    def test_centroid(self):
        from geojson_utils import centroid
        box_str = '{"type": "Polygon","coordinates": [[ [0, 0], [10, 0], [10, 10], [0, 10] ]]}'
        box = json.loads(box_str)
        self.assertEqual(centroid(box), {"type": "Point", "coordinates": [5, 5]})

    def test_destination_point(self):
        from geojson_utils import destination_point
        startpoint_str = '{"type": "Point", "coordinates":  [-122.260000705719, 37.80919060818706]}'
        startpoint = json.loads(startpoint_str)
        self.assertEqual(destination_point(startpoint, 180, 2000)["coordinates"][0], -122.26000070571902)

    def test_distance_ellipsode(self):
        from geojson_utils import point_distance_ellipsode
        fairyland_str = '{"type": "Point", "coordinates": [-122.260000705719, 37.80919060818706]}'
        navalbase_str = '{"type": "Point", "coordinates": [-122.32083320617676, 37.78774223089045]}'
        fairyland = json.loads(fairyland_str)
        navalbase = json.loads(navalbase_str)
        print(point_distance_ellipsode(fairyland,navalbase)) 
        
    def test_json_featurecollection(self):
        from geojson_utils import join_featurecollection
        with open('tests/first.json','r') as fp:
            first = json.load(fp)
        with open('tests/second.json','r') as fp:
            second = json.load(fp)
        with open('tests/result.json','r') as fp:
            result = json.load(fp)
        self.assertEqual(join_featurecollection(first,second),result)
    

if __name__ == '__main__':
    unittest.main()
