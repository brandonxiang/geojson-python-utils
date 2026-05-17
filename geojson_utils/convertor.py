from copy import deepcopy
from typing import Any, Callable, Dict, List, MutableMapping, Sequence
from .coordTransform_utils import wgs84togcj02, gcj02towgs84, gcj02tobd09, bd09togcj02

Coordinate = List[float]
GeoJSON = MutableMapping[str, Any]


def wgs84tobd09(lng: float, lat: float) -> Coordinate:
    """Convert a WGS84 coordinate to BD-09 through GCJ-02."""
    tmp_lng, tmp_lat = wgs84togcj02(lng, lat)
    return gcj02tobd09(tmp_lng, tmp_lat)


def bd09towgs84(lng: float, lat: float) -> Coordinate:
    """Convert a BD-09 coordinate to WGS84 through GCJ-02."""
    tmp_lng, tmp_lat = bd09togcj02(lng, lat)
    return gcj02towgs84(tmp_lng, tmp_lat)

methods: Dict[str, Callable[[float, float], Coordinate]] = {
    "wgs2gcj": wgs84togcj02,
    "gcj2wgs": gcj02towgs84,
    "wgs2bd": wgs84tobd09,
    "bd2wgs": bd09towgs84,
    "gcj2bd": gcj02tobd09,
    "bd2gcj": bd09togcj02
}


def _convert_position(coords: Sequence[float], method: str) -> Coordinate:
    lng, lat = methods[method](coords[0], coords[1])
    converted = [lng, lat]
    converted.extend(coords[2:])
    return converted


def _convert_geometry(geometry: GeoJSON, method: str) -> GeoJSON:
    if method not in methods:
        raise ValueError(f"unsupported coordinate conversion method: {method}")

    if geometry['type'] == 'Point':
        geometry['coordinates'] = _convert_position(geometry['coordinates'], method)
    elif geometry['type'] == 'LineString' or geometry['type'] == 'MultiPoint':
        geometry['coordinates'] = [_convert_position(coords, method) for coords in geometry['coordinates']]
    elif geometry['type'] == 'Polygon' or geometry['type'] == 'MultiLineString':
        geometry['coordinates'] = [
            [_convert_position(coords, method) for coords in rings]
            for rings in geometry['coordinates']
        ]
    elif geometry['type'] == 'MultiPolygon':
        geometry['coordinates'] = [
            [
                [_convert_position(coords, method) for coords in lines]
                for lines in rings
            ]
            for rings in geometry['coordinates']
        ]
    elif geometry['type'] == 'GeometryCollection':
        geometry['geometries'] = [_convert_geometry(child, method) for child in geometry.get('geometries', [])]
    return geometry


def convertor(geometry: GeoJSON, method: str = "wgs2gcj", inplace: bool = True) -> GeoJSON:
    """
    Convert coordinates in a GeoJSON object.

    Geometry, Feature, FeatureCollection, and GeometryCollection inputs are
    supported. By default the input object is mutated for backwards
    compatibility. Pass `inplace=False` to return a converted copy.

    referencing by https://github.com/wandergis/coordTransform_py
    """
    target = geometry if inplace else deepcopy(geometry)
    target_type = target['type']
    if target_type == 'Feature':
        if target.get('geometry') is not None:
            target['geometry'] = _convert_geometry(target['geometry'], method)
    elif target_type == 'FeatureCollection':
        for feature in target.get('features', []):
            if feature.get('geometry') is not None:
                feature['geometry'] = _convert_geometry(feature['geometry'], method)
    else:
        _convert_geometry(target, method)
    return target
