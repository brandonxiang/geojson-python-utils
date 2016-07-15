from .coordTransform_utils import wgs84togcj02

def wgs2gcj(geometry):
    """
    convert wgs84 to gcj
    referencing by https://github.com/wandergis/coordTransform_py
    """
    # TODO: point linestring point
    if geometry['type'] == 'MultiLineString':
        coordinates = geometry['coordinates']
        for line in coordinates:
            line[0], line[1] = wgs84togcj02(line[0], line[1])

    return geometry