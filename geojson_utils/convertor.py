from .coordTransform_utils import wgs84togcj02, gcj02towgs84, gcj02tobd09, bd09togcj02


def wgs84tobd09(lng, lat):
    tmp_lng, tmp_lat = wgs84togcj02(lng, lat)
    return gcj02tobd09(tmp_lng, tmp_lat)


def bd09towgs84(lng, lat):
    tmp_lng, tmp_lat = bd09togcj02(lng, lat)
    return gcj02towgs84(tmp_lng, tmp_lat)

methods = {
    "wgs2gcj": wgs84togcj02,
    "gcj2wgs": gcj02towgs84,
    "wgs2bd": wgs84tobd09,
    "bd2wgs": bd09towgs84,
    "gcj2bd": gcj02tobd09,
    "bd2gcj": bd09towgs84
}


def convertor(geometry, method="wgs2gcj"):
    """
    convert wgs84 to gcj
    referencing by https://github.com/wandergis/coordTransform_py
    """
    if geometry['type'] == 'Point':
        coords = geometry['coordinates']
        coords[0], coords[1] = methods[method](coords[0], coords[1])
    elif geometry['type'] == 'LineString' or geometry['type'] == 'MutliPoint':
        coordinates = geometry['coordinates']
        for coords in coordinates:
            coords[0], coords[1] = methods[method](coords[0], coords[1])
    elif geometry['type'] == 'Polygon' or geometry['type'] == 'MultiLineString':
        coordinates = geometry['coordinates']
        for rings in coordinates:
            for coords in rings:
                coords[0], coords[1] = methods[method](coords[0], coords[1])
    elif geometry['type'] == 'MultiPolygon':
        coordinates = geometry['coordinates']
        for rings in coordinates:
            for lines in rings:
                for coords in lines:
                    coords[0], coords[1] = methods[method](coords[0], coords[1])
    return geometry


