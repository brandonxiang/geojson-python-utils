import json
import math


def linestrings_intersect(l1, l2):
    """
    bounding box
    """
    intersects = []
    for i in range(0, len(l1['coordinates']) - 1):
        for j in range(0, len(l2['coordinates']) - 1):
            a1_x = l1['coordinates'][i][1]
            a1_y = l1['coordinates'][i][0]
            a2_x = l1['coordinates'][i + 1][1]
            a2_y = l1['coordinates'][i + 1][0]
            b1_x = l2['coordinates'][j][1]
            b1_y = l2['coordinates'][j][0]
            b2_x = l2['coordinates'][j + 1][1]
            b2_y = l2['coordinates'][j + 1][0]
            ua_t = (b2_x - b1_x) * (a1_y - b1_y) - (b2_y - b1_y) * (a1_x - b1_x)
            ub_t = (a2_x - a1_x) * (a1_y - b1_y) - (a2_y - a1_y) * (a1_x - b1_x)
            u_b = (b2_y - b1_y) * (a2_x - a1_x) - (b2_x - b1_x) * (a2_y - a1_y)
            if not u_b == 0:
                u_a = ua_t / u_b
                u_b = ub_t / u_b
                if 0 <= u_a and u_a <= 1 and 0 <= u_b and u_b <= 1:
                    intersects.append({'type': 'Point', 'coordinates': [a1_x + u_a * (a2_x - a1_x), a1_y + u_a * (a2_y - a1_y)]})
    if len(intersects) == 0:
        intersects = False
    return intersects


def bbox_around_polycoords(coords):
    """
    bounding box
    """
    x_all = []
    y_all = []

    for first in coords[0]:
        x_all.append(first[1])
        y_all.append(first[0])

    return [min(x_all), min(y_all), max(x_all), max(y_all)]


def point_in_bbox(point, bounds):
    """
    whether the point is inside the bounding box
    """
    return not(point['coordinates'][1] < bounds[0] or point['coordinates'][1] > bounds[2] \
     or point['coordinates'][0] < bounds[1] or point['coordinates'][0] > bounds[3])


def pnpoly(x, y, coords):
    """
    point in polygon algorithem
    reference: https://www.ecse.rpi.edu/~wrf/Research/Short_Notes/pnpoly.html#Explanation
    """
    vert = [[0, 0]]

    for coord in coords:
        for node in coord:
            vert.append(node)
        vert.append(coord[0])
        vert.append([0, 0])

    inside = False

    i = 0
    j = len(vert) - 1

    while i < len(vert):
        if ((vert[i][0] > y) != (vert[j][0] > y)) and (x < (vert[j][1] - vert[i][1]) \
         * (y - vert[i][0]) / (vert[j][0] - vert[i][0]) + vert[i][1]):
            inside = not inside
        j = i
        i += 1

    return inside


def point_in_polygon(point, poly):
    """
    main point in polygon function
    """
    coords = [poly['coordinates']] if poly['type'] == 'Polygon' else poly['coordinates']
    inside_box = False
    for coord in coords:
        if point_in_bbox(point, bbox_around_polycoords(coord)):
            inside_box = True
    if not inside_box:
        return False

    inside_poly = False
    for coord in coords:
        if pnpoly(point['coordinates'][1], point['coordinates'][0], coord):
            inside_poly = True

    return inside_poly

def number2radius(number):
    """
    convert degree into radius
    """
    return number*math.pi /180

def number2degree(number):
    """
    convert radius into degree
    """
    return number* 180/math.pi


def test():
    """
    test for geojson-python-utils
    """
    diagonal_up_str = '{ "type": "LineString","coordinates": [[0, 0], [10, 10]]}'
    diagonal_down_str = '{ "type": "LineString","coordinates": [[10, 0], [0, 10]]}'
    far_away_str = '{ "type": "LineString","coordinates": [[100, 100], [110, 110]]}'
    diagonal_up = json.loads(diagonal_up_str)
    diagonal_down = json.loads(diagonal_down_str)
    far_away = json.loads(far_away_str)
    print "intersect:%s" % ('True' if linestrings_intersect(diagonal_up, diagonal_down) else 'False')
    print "not intersect:%s" % ('True' if linestrings_intersect(diagonal_up, far_away) else 'False')

    in_str = '{"type": "Point", "coordinates": [5, 5]}'
    out_str = '{"type": "Point", "coordinates": [15, 15]}'
    box_str = '{"type": "Polygon","coordinates": [[ [0, 0], [10, 0], [10, 10], [0, 10] ]]}'
    in_box = json.loads(in_str)
    out_box = json.loads(out_str)
    box = json.loads(box_str)
    print "inbox : %s " % ('True' if point_in_polygon(in_box, box) else 'False')
    print "outbox : %s" % ('True' if point_in_polygon(out_box, box) else 'False')

if __name__ == '__main__':
    test()
