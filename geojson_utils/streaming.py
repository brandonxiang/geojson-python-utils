import json
from typing import Any, Iterable, Iterator, TextIO

from .validation import GeoJSON, validate_feature, validate_geojson


def iter_features(value: GeoJSON) -> Iterator[GeoJSON]:
    """Yield Feature objects from a Feature or FeatureCollection."""
    value = validate_geojson(value)
    if value["type"] == "Feature":
        yield value
    elif value["type"] == "FeatureCollection":
        for feature in value.get("features", []):
            yield feature
    else:
        yield {"type": "Feature", "geometry": value, "properties": {}}


def read_ndjson_features(source: TextIO) -> Iterator[GeoJSON]:
    """Yield GeoJSON Features from newline-delimited JSON."""
    for line_number, line in enumerate(source, start=1):
        line = line.strip()
        if not line:
            continue
        try:
            feature = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_number}: invalid JSON") from exc
        yield validate_feature(feature, path=f"line {line_number}")


def write_ndjson_features(features: Iterable[GeoJSON], target: TextIO) -> None:
    """Write GeoJSON Features as newline-delimited JSON."""
    for feature in features:
        validate_feature(feature)
        target.write(json.dumps(feature, ensure_ascii=False, separators=(",", ":")))
        target.write("\n")


def feature_collection_from_iter(features: Iterable[GeoJSON]) -> GeoJSON:
    """Build a FeatureCollection from an iterable of Features."""
    return {"type": "FeatureCollection", "features": [validate_feature(feature) for feature in features]}
