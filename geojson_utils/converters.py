import json
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Optional, Tuple

from .validation import GeoJSON, validate_geojson
from .csv_adapter import csv_to_feature_collection, feature_collection_to_csv
from .file_adapters import read_geopackage, read_shapefile, write_geopackage, write_shapefile
from .wkt import geojson_to_wkb, geojson_to_wkt, wkb_to_geojson, wkt_to_geojson

Converter = Callable[[Any], Any]
FormatPair = Tuple[str, str]

_converters: Dict[FormatPair, Converter] = {}


class GeoJSONConversionError(ValueError):
    """Raised when a conversion cannot be completed."""


def _normalize_format(format_name: str) -> str:
    return format_name.strip().lower().replace("_", "-")


def register_converter(from_format: str, to_format: str, converter: Converter) -> None:
    """Register a converter callable for a source and target format pair."""
    _converters[(_normalize_format(from_format), _normalize_format(to_format))] = converter


def registered_converters() -> Iterable[FormatPair]:
    """Return registered conversion pairs."""
    return tuple(sorted(_converters))


def convert(value: Any, from_format: str, to_format: str) -> Any:
    """Convert a value between registered formats."""
    source = _normalize_format(from_format)
    target = _normalize_format(to_format)

    if source == target:
        return value

    converter = _converters.get((source, target))
    if converter is None:
        raise GeoJSONConversionError(f"no converter registered for {source!r} -> {target!r}")
    return converter(value)


def read_geojson(path: str, *, encoding: str = "utf-8") -> GeoJSON:
    """Read and validate a GeoJSON file."""
    with open(path, encoding=encoding) as fp:
        return validate_geojson(json.load(fp))


def write_geojson(value: GeoJSON, path: str, *, encoding: str = "utf-8", indent: Optional[int] = 2) -> None:
    """Validate and write a GeoJSON file."""
    validate_geojson(value)
    with open(path, "w", encoding=encoding) as fp:
        json.dump(value, fp, ensure_ascii=False, indent=indent)
        fp.write("\n")


def load_geojson_text(value: str) -> GeoJSON:
    """Parse and validate GeoJSON from a JSON string."""
    return validate_geojson(json.loads(value))


def dump_geojson_text(value: GeoJSON) -> str:
    """Serialize a validated GeoJSON object to a compact JSON string."""
    validate_geojson(value)
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def read_geojson_auto(value: Any) -> GeoJSON:
    """Read GeoJSON from an object, JSON text, or a filesystem path."""
    if isinstance(value, dict):
        return validate_geojson(value)
    if isinstance(value, (str, Path)):
        text = str(value)
        if text.lstrip().startswith("{"):
            return load_geojson_text(text)
        return read_geojson(text)
    raise GeoJSONConversionError(f"cannot read GeoJSON from {type(value).__name__}")


def _geojson_to_geojson(value: Any) -> GeoJSON:
    return read_geojson_auto(value)


def _geojson_to_json_text(value: Any) -> str:
    return dump_geojson_text(read_geojson_auto(value))


def _json_text_to_geojson(value: str) -> GeoJSON:
    return load_geojson_text(value)


register_converter("geojson", "json", _geojson_to_json_text)
register_converter("json", "geojson", _json_text_to_geojson)
register_converter("geojson-file", "geojson", read_geojson)
register_converter("geojson", "geojson-file", lambda value: value)
register_converter("geojson", "wkt", lambda value: geojson_to_wkt(read_geojson_auto(value)))
register_converter("wkt", "geojson", wkt_to_geojson)
register_converter("geojson", "wkb", lambda value: geojson_to_wkb(read_geojson_auto(value)))
register_converter("wkb", "geojson", wkb_to_geojson)
register_converter("csv", "geojson", csv_to_feature_collection)
register_converter("geojson", "csv", lambda value: feature_collection_to_csv(read_geojson_auto(value)))
register_converter("shapefile", "geojson", read_shapefile)
register_converter("geojson", "shapefile", write_shapefile)
register_converter("geopackage", "geojson", read_geopackage)
register_converter("geojson", "geopackage", write_geopackage)
