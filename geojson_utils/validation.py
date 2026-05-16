from copy import deepcopy
from typing import Any, Dict, Iterable, List, MutableMapping, Optional, Sequence, Tuple

GeoJSON = MutableMapping[str, Any]
Coordinate = List[float]
Ring = List[Coordinate]


class GeoJSONValidationError(ValueError):
    """Raised when a GeoJSON object is structurally invalid."""


def _fail(path: str, message: str) -> None:
    raise GeoJSONValidationError(f"{path}: {message}")


def _require_mapping(value: Any, path: str) -> GeoJSON:
    if not isinstance(value, dict):
        _fail(path, "expected an object")
    return value


def _require_number(value: Any, path: str) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        _fail(path, "expected a number")


def _validate_position(value: Any, path: str) -> None:
    if not isinstance(value, list):
        _fail(path, "expected a coordinate array")
    if len(value) < 2:
        _fail(path, "expected at least longitude and latitude")
    for index, number in enumerate(value):
        _require_number(number, f"{path}[{index}]")


def _validate_positions(value: Any, depth: int, path: str) -> None:
    if depth == 0:
        _validate_position(value, path)
        return
    if not isinstance(value, list):
        _fail(path, "expected an array")
    if len(value) == 0:
        _fail(path, "expected a non-empty array")
    for index, item in enumerate(value):
        _validate_positions(item, depth - 1, f"{path}[{index}]")


def _validate_ring(ring: Any, path: str) -> None:
    if not isinstance(ring, list):
        _fail(path, "expected a linear ring")
    if len(ring) < 4:
        _fail(path, "linear rings need at least four positions")
    for index, coordinate in enumerate(ring):
        _validate_position(coordinate, f"{path}[{index}]")
    if ring[0][:2] != ring[-1][:2]:
        _fail(path, "linear ring must be closed")


def _validate_polygon_coordinates(coordinates: Any, path: str) -> None:
    if not isinstance(coordinates, list) or len(coordinates) == 0:
        _fail(path, "expected a non-empty polygon coordinate array")
    for index, ring in enumerate(coordinates):
        _validate_ring(ring, f"{path}[{index}]")


def _validate_geometry_collection(geometry: GeoJSON, path: str) -> None:
    geometries = geometry.get("geometries")
    if not isinstance(geometries, list):
        _fail(f"{path}.geometries", "expected an array")
    for index, child in enumerate(geometries):
        validate_geometry(child, f"{path}.geometries[{index}]")


def validate_geometry(geometry: Any, path: str = "$") -> GeoJSON:
    """Validate a GeoJSON Geometry object and return it unchanged."""
    geometry = _require_mapping(geometry, path)
    geometry_type = geometry.get("type")
    if not isinstance(geometry_type, str):
        _fail(f"{path}.type", "expected a geometry type string")

    if geometry_type == "GeometryCollection":
        _validate_geometry_collection(geometry, path)
        return geometry

    if "coordinates" not in geometry:
        _fail(f"{path}.coordinates", "missing coordinates")
    coordinates = geometry["coordinates"]

    if geometry_type == "Point":
        _validate_position(coordinates, f"{path}.coordinates")
    elif geometry_type in ("MultiPoint", "LineString"):
        _validate_positions(coordinates, 1, f"{path}.coordinates")
    elif geometry_type in ("MultiLineString",):
        _validate_positions(coordinates, 2, f"{path}.coordinates")
    elif geometry_type == "Polygon":
        _validate_polygon_coordinates(coordinates, f"{path}.coordinates")
    elif geometry_type == "MultiPolygon":
        if not isinstance(coordinates, list) or len(coordinates) == 0:
            _fail(f"{path}.coordinates", "expected a non-empty multipolygon coordinate array")
        for index, polygon in enumerate(coordinates):
            _validate_polygon_coordinates(polygon, f"{path}.coordinates[{index}]")
    else:
        _fail(f"{path}.type", f"unsupported geometry type {geometry_type!r}")

    return geometry


def validate_feature(feature: Any, path: str = "$") -> GeoJSON:
    """Validate a GeoJSON Feature object and return it unchanged."""
    feature = _require_mapping(feature, path)
    if feature.get("type") != "Feature":
        _fail(f"{path}.type", "expected 'Feature'")
    if "geometry" not in feature:
        _fail(f"{path}.geometry", "missing geometry")
    if feature["geometry"] is not None:
        validate_geometry(feature["geometry"], f"{path}.geometry")
    if "properties" in feature and feature["properties"] is not None and not isinstance(feature["properties"], dict):
        _fail(f"{path}.properties", "expected an object or null")
    return feature


def validate_feature_collection(collection: Any, path: str = "$") -> GeoJSON:
    """Validate a GeoJSON FeatureCollection object and return it unchanged."""
    collection = _require_mapping(collection, path)
    if collection.get("type") != "FeatureCollection":
        _fail(f"{path}.type", "expected 'FeatureCollection'")
    features = collection.get("features")
    if not isinstance(features, list):
        _fail(f"{path}.features", "expected an array")
    for index, feature in enumerate(features):
        validate_feature(feature, f"{path}.features[{index}]")
    return collection


def validate_geojson(value: Any, path: str = "$") -> GeoJSON:
    """Validate any GeoJSON object and return it unchanged."""
    value = _require_mapping(value, path)
    value_type = value.get("type")
    if value_type == "Feature":
        return validate_feature(value, path)
    if value_type == "FeatureCollection":
        return validate_feature_collection(value, path)
    return validate_geometry(value, path)


def _ring_area(ring: Sequence[Sequence[float]]) -> float:
    total = 0.0
    for index, point in enumerate(ring):
        next_point = ring[(index + 1) % len(ring)]
        total += point[0] * next_point[1] - next_point[0] * point[1]
    return total / 2.0


def _normalize_ring(ring: Iterable[Sequence[float]], clockwise: Optional[bool]) -> Ring:
    normalized = [list(coordinate) for coordinate in ring]
    if normalized and normalized[0][:2] != normalized[-1][:2]:
        normalized.append(list(normalized[0]))
    if clockwise is not None and len(normalized) >= 4:
        is_clockwise = _ring_area(normalized) < 0
        if is_clockwise != clockwise:
            normalized.reverse()
    return normalized


def _normalize_geometry(geometry: GeoJSON, close_rings: bool, orient_rings: bool) -> GeoJSON:
    geometry_type = geometry.get("type")
    if geometry_type == "Polygon":
        rings = geometry["coordinates"]
        if close_rings or orient_rings:
            geometry["coordinates"] = [
                _normalize_ring(ring, clockwise=(index > 0 if orient_rings else None))
                for index, ring in enumerate(rings)
            ]
    elif geometry_type == "MultiPolygon":
        polygons = geometry["coordinates"]
        if close_rings or orient_rings:
            geometry["coordinates"] = [
                [
                    _normalize_ring(ring, clockwise=(index > 0 if orient_rings else None))
                    for index, ring in enumerate(polygon)
                ]
                for polygon in polygons
            ]
    elif geometry_type == "GeometryCollection":
        geometry["geometries"] = [
            _normalize_geometry(child, close_rings, orient_rings) for child in geometry.get("geometries", [])
        ]
    return geometry


def normalize_geojson(
    value: GeoJSON,
    *,
    close_rings: bool = True,
    orient_rings: bool = False,
    keep_bbox: bool = True,
    keep_id: bool = True,
) -> GeoJSON:
    """
    Return a normalized copy of a GeoJSON object.

    Polygon rings can be closed and oriented. Exterior rings are normalized to
    counter-clockwise and holes to clockwise when `orient_rings` is enabled.
    """
    normalized = deepcopy(value)
    normalized_type = normalized.get("type")

    if not keep_bbox:
        normalized.pop("bbox", None)
    if not keep_id:
        normalized.pop("id", None)

    if normalized_type == "Feature":
        if not keep_bbox:
            normalized.get("geometry", {}).pop("bbox", None)
        if normalized.get("geometry") is not None:
            _normalize_geometry(normalized["geometry"], close_rings, orient_rings)
    elif normalized_type == "FeatureCollection":
        for feature in normalized.get("features", []):
            if not keep_bbox:
                feature.pop("bbox", None)
                feature.get("geometry", {}).pop("bbox", None)
            if not keep_id:
                feature.pop("id", None)
            if feature.get("geometry") is not None:
                _normalize_geometry(feature["geometry"], close_rings, orient_rings)
    else:
        _normalize_geometry(normalized, close_rings, orient_rings)

    return validate_geojson(normalized)
