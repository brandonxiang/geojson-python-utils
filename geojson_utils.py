import json


def boundingBoxAroundPolyCoords(coords):
    """
    bounding box
    """
    x_all = []
    y_all = []

    for first in coords[0]:
        x_all.append(first[1])
        y_all.append(first[0])

    return [min(x_all), min(y_all), max(x_all), max(y_all)]


def pointInBoundingBox(point, bounds):
    """
    whether the point is inside the bounding box
    """
    return not(point['coordinates'][1] < bounds[0] or point['coordinates'][1] > bounds[2] or point['coordinates'][0] < bounds[1] or point['coordinates'][0] > bounds[3])


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
        if ((vert[i][0] > y) != (vert[j][0] > y)) and (x < (vert[j][1] - vert[i][1]) * (y - vert[i][0]) / (vert[j][0] - vert[i][0]) + vert[i][1]):
            inside = not inside
        j = i
        i += 1

    return inside


def pointInPolygon(p, poly):
    """
    main point in polygon function
    """
    coords = [poly['coordinates']] if poly['type'] == 'Polygon' else poly['coordinates']
    inside_box = False
    for coord in coords:
        if pointInBoundingBox(p, boundingBoxAroundPolyCoords(coord)):
            inside_box = True
    if not inside_box:
        return False

    inside_poly = False
    for coord in coords:
        if pnpoly(p['coordinates'][1], p['coordinates'][0], coord):
            inside_poly = True

    return inside_poly


def test():
    in_str = '{"type": "Point", "coordinates": [5, 5]}'
    out_str = '{"type": "Point", "coordinates": [15, 15]}'
    box_str = '{"type": "Polygon","coordinates": [[ [0, 0], [10, 0], [10, 10], [0, 10] ]]}'
    in_box = json.loads(in_str)
    out_box = json.loads(out_str)
    box = json.loads(box_str)
    print pointInPolygon(in_box, box)
    print pointInPolygon(out_box, box)

if __name__ == '__main__':
    test()
