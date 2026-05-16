from typing import Any, Iterable, List, MutableMapping, Sequence

GeoJSON = MutableMapping[str, Any]
BBox = List[float]


def iter_coordinates(value: Any) -> Iterable[Sequence[float]]:
    """Yield coordinate positions from any GeoJSON object."""
    if not isinstance(value, dict):
        return
    value_type = value.get("type")
    if value_type == "FeatureCollection":
        for feature in value.get("features", []):
            yield from iter_coordinates(feature)
    elif value_type == "Feature":
        yield from iter_coordinates(value.get("geometry"))
    elif value_type == "GeometryCollection":
        for geometry in value.get("geometries", []):
            yield from iter_coordinates(geometry)
    elif value_type == "Point":
        yield value["coordinates"]
    elif value_type in ("MultiPoint", "LineString"):
        for coordinate in value["coordinates"]:
            yield coordinate
    elif value_type in ("MultiLineString", "Polygon"):
        for line in value["coordinates"]:
            for coordinate in line:
                yield coordinate
    elif value_type == "MultiPolygon":
        for polygon in value["coordinates"]:
            for ring in polygon:
                for coordinate in ring:
                    yield coordinate


def bbox(value: GeoJSON) -> BBox:
    """Return [min_lon, min_lat, max_lon, max_lat] for a GeoJSON object."""
    coordinates = list(iter_coordinates(value))
    if not coordinates:
        raise ValueError("cannot calculate bbox for empty GeoJSON")
    xs = [coordinate[0] for coordinate in coordinates]
    ys = [coordinate[1] for coordinate in coordinates]
    return [min(xs), min(ys), max(xs), max(ys)]


def intersects_bbox(left: Sequence[float], right: Sequence[float]) -> bool:
    """Return whether two bbox arrays intersect."""
    return not (left[2] < right[0] or left[0] > right[2] or left[3] < right[1] or left[1] > right[3])


def filter_features_by_bbox(collection: GeoJSON, bounds: Sequence[float]) -> GeoJSON:
    """Return a FeatureCollection containing features whose bbox intersects bounds."""
    if collection.get("type") != "FeatureCollection":
        raise ValueError("expected a FeatureCollection")
    features = []
    for feature in collection.get("features", []):
        if intersects_bbox(bbox(feature), bounds):
            features.append(feature)
    return {"type": "FeatureCollection", "features": features}


class BBoxIndex:
    """Small in-memory bbox index for FeatureCollection filtering."""

    def __init__(self, collection: GeoJSON):
        if collection.get("type") != "FeatureCollection":
            raise ValueError("expected a FeatureCollection")
        self._features = [(bbox(feature), feature) for feature in collection.get("features", [])]

    def search(self, bounds: Sequence[float]) -> GeoJSON:
        features = [feature for feature_bounds, feature in self._features if intersects_bbox(feature_bounds, bounds)]
        return {"type": "FeatureCollection", "features": features}
