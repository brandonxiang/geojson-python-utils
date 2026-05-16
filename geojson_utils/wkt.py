from typing import Any, List, MutableMapping, Sequence

GeoJSON = MutableMapping[str, Any]


class WKTError(ValueError):
    """Raised when WKT cannot be parsed or written."""


def _format_number(value: float) -> str:
    return ("%f" % value).rstrip("0").rstrip(".")


def _format_position(position: Sequence[float]) -> str:
    return " ".join(_format_number(number) for number in position)


def _format_line(coordinates: Sequence[Sequence[float]]) -> str:
    return ", ".join(_format_position(position) for position in coordinates)


def geojson_to_wkt(geometry: GeoJSON) -> str:
    """Serialize a GeoJSON Geometry dictionary to WKT."""
    geometry_type = geometry["type"]
    coordinates = geometry.get("coordinates")

    if geometry_type == "Point":
        return "POINT (%s)" % _format_position(coordinates)
    if geometry_type == "MultiPoint":
        return "MULTIPOINT (%s)" % ", ".join("(%s)" % _format_position(point) for point in coordinates)
    if geometry_type == "LineString":
        return "LINESTRING (%s)" % _format_line(coordinates)
    if geometry_type == "MultiLineString":
        return "MULTILINESTRING (%s)" % ", ".join("(%s)" % _format_line(line) for line in coordinates)
    if geometry_type == "Polygon":
        return "POLYGON (%s)" % ", ".join("(%s)" % _format_line(ring) for ring in coordinates)
    if geometry_type == "MultiPolygon":
        polygons = []
        for polygon in coordinates:
            polygons.append("(%s)" % ", ".join("(%s)" % _format_line(ring) for ring in polygon))
        return "MULTIPOLYGON (%s)" % ", ".join(polygons)
    if geometry_type == "GeometryCollection":
        return "GEOMETRYCOLLECTION (%s)" % ", ".join(geojson_to_wkt(child) for child in geometry.get("geometries", []))
    raise WKTError(f"unsupported geometry type {geometry_type!r}")


def _strip_outer(value: str) -> str:
    value = value.strip()
    if not (value.startswith("(") and value.endswith(")")):
        raise WKTError("expected parenthesized WKT body")
    return value[1:-1].strip()


def _split_top_level(value: str) -> List[str]:
    parts = []
    start = 0
    depth = 0
    for index, char in enumerate(value):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            parts.append(value[start:index].strip())
            start = index + 1
    parts.append(value[start:].strip())
    return [part for part in parts if part]


def _parse_position(value: str) -> List[float]:
    try:
        return [float(number) for number in value.strip().split()]
    except ValueError as exc:
        raise WKTError(f"invalid coordinate {value!r}") from exc


def _parse_line(value: str) -> List[List[float]]:
    return [_parse_position(part) for part in _split_top_level(value)]


def wkt_to_geojson(value: str) -> GeoJSON:
    """Parse a WKT geometry string into a GeoJSON Geometry dictionary."""
    text = value.strip()
    type_name, _, body = text.partition(" ")
    geometry_type = type_name.upper()
    body = body.strip()

    if geometry_type == "POINT":
        return {"type": "Point", "coordinates": _parse_position(_strip_outer(body))}
    if geometry_type == "MULTIPOINT":
        points = [_parse_position(_strip_outer(part)) for part in _split_top_level(_strip_outer(body))]
        return {"type": "MultiPoint", "coordinates": points}
    if geometry_type == "LINESTRING":
        return {"type": "LineString", "coordinates": _parse_line(_strip_outer(body))}
    if geometry_type == "MULTILINESTRING":
        lines = [_parse_line(_strip_outer(part)) for part in _split_top_level(_strip_outer(body))]
        return {"type": "MultiLineString", "coordinates": lines}
    if geometry_type == "POLYGON":
        rings = [_parse_line(_strip_outer(part)) for part in _split_top_level(_strip_outer(body))]
        return {"type": "Polygon", "coordinates": rings}
    if geometry_type == "MULTIPOLYGON":
        polygons = []
        for polygon in _split_top_level(_strip_outer(body)):
            rings = [_parse_line(_strip_outer(part)) for part in _split_top_level(_strip_outer(polygon))]
            polygons.append(rings)
        return {"type": "MultiPolygon", "coordinates": polygons}
    if geometry_type == "GEOMETRYCOLLECTION":
        return {
            "type": "GeometryCollection",
            "geometries": [wkt_to_geojson(part) for part in _split_top_level(_strip_outer(body))],
        }
    raise WKTError(f"unsupported WKT geometry type {geometry_type!r}")


def geojson_to_wkb(geometry: GeoJSON) -> bytes:
    """Convert GeoJSON to WKB through optional Shapely support."""
    try:
        from shapely.geometry import shape
    except ImportError as exc:
        raise WKTError("WKB support requires the optional 'shapely' dependency") from exc
    return shape(geometry).wkb


def wkb_to_geojson(value: bytes) -> GeoJSON:
    """Convert WKB bytes to GeoJSON through optional Shapely support."""
    try:
        from shapely import wkb
        from shapely.geometry import mapping
    except ImportError as exc:
        raise WKTError("WKB support requires the optional 'shapely' dependency") from exc
    return dict(mapping(wkb.loads(value)))
