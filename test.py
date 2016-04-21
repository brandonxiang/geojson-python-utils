import json
import math
from geojson_utils import linestrings_intersect
from geojson_utils import point_in_polygon
from geojson_utils import point_in_multipolygon
from geojson_utils import draw_circle
from geojson_utils import rectangle_centroid
from geojson_utils import point_distance


def _test():
    #linestrings intersect
    diagonal_up_str = '{ "type": "LineString","coordinates": [[0, 0], [10, 10]]}'
    diagonal_down_str = '{ "type": "LineString","coordinates": [[10, 0], [0, 10]]}'
    far_away_str = '{ "type": "LineString","coordinates": [[100, 100], [110, 110]]}'
    diagonal_up = json.loads(diagonal_up_str)
    diagonal_down = json.loads(diagonal_down_str)
    far_away = json.loads(far_away_str)
    print linestrings_intersect(diagonal_up, diagonal_down)
    print linestrings_intersect(diagonal_up, far_away)

    #point in polygon
    in_str = '{"type": "Point", "coordinates": [5, 5]}'
    out_str = '{"type": "Point", "coordinates": [15, 15]}'
    box_str = '{"type": "Polygon","coordinates": [[ [0, 0], [10, 0], [10, 10], [0, 10] ]]}'
    in_box = json.loads(in_str)
    out_box = json.loads(out_str)
    box = json.loads(box_str)

    assert point_in_polygon(in_box, box) is True
    assert point_in_polygon(out_box, box) is False

    #point in multipolygon
    point_str = '{"type": "Point", "coordinates": [0.5, 0.5]}'
    single_point_str = '{"type": "Point", "coordinates": [-1, -1]}'
    multipoly_str = '{"type":"MultiPolygon","coordinates":[[[[0,0],[0,10],[10,10],[10,0],[0,0]]],[[[10,10],[10,20],[20,20],[20,10],[10,10]]]]}'
    point = json.loads(point_str)
    single_point = json.loads(single_point_str)
    multipoly = json.loads(multipoly_str)
    assert  point_in_multipolygon(point, multipoly) is True
    assert point_in_multipolygon(single_point, multipoly) is False

    #drawCircle
    pt_center = json.loads('{"type": "Point", "coordinates": [0, 0]}')
    assert len(draw_circle(10, pt_center)['coordinates'][0]) == 15
    assert len(draw_circle(10, pt_center, 50)['coordinates'][0]) == 50

    #rectangle_centroid
    centroid = rectangle_centroid(box)
    assert centroid['coordinates'] == [5, 5]

    #point_distance
    fairyland_str = '{"type": "Point", "coordinates": [-122.260000705719, 37.80919060818706]}'
    navalbase_str = '{"type": "Point", "coordinates": [-122.32083320617676, 37.78774223089045]}'
    fairyland = json.loads(fairyland_str)
    navalbase = json.loads(navalbase_str)
    assert math.floor(point_distance(fairyland, navalbase)) == 5852


if __name__ == '__main__':
    _test()
