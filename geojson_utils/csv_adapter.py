import csv
from io import StringIO
from typing import Any, Dict, Iterable, List, MutableMapping, Optional

GeoJSON = MutableMapping[str, Any]


class CSVGeoJSONError(ValueError):
    """Raised when CSV point conversion fails."""


def csv_to_feature_collection(
    text: str,
    *,
    longitude: str = "longitude",
    latitude: str = "latitude",
    id_column: Optional[str] = None,
) -> GeoJSON:
    """Convert CSV point rows to a GeoJSON FeatureCollection."""
    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise CSVGeoJSONError("CSV header is required")
    missing = [column for column in (longitude, latitude) if column not in reader.fieldnames]
    if missing:
        raise CSVGeoJSONError("missing coordinate columns: %s" % ", ".join(missing))

    features: List[GeoJSON] = []
    for line_number, row in enumerate(reader, start=2):
        lng_value = row.get(longitude, "")
        lat_value = row.get(latitude, "")
        if lng_value == "" or lat_value == "":
            raise CSVGeoJSONError(f"line {line_number}: missing coordinate value")
        try:
            coordinates = [float(lng_value), float(lat_value)]
        except ValueError as exc:
            raise CSVGeoJSONError(f"line {line_number}: invalid coordinate value") from exc

        properties: Dict[str, Any] = {
            key: value
            for key, value in row.items()
            if key not in (longitude, latitude) and key != id_column
        }
        feature: GeoJSON = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": coordinates},
            "properties": properties,
        }
        if id_column and row.get(id_column):
            feature["id"] = row[id_column]
        features.append(feature)

    return {"type": "FeatureCollection", "features": features}


def feature_collection_to_csv(
    collection: GeoJSON,
    *,
    longitude: str = "longitude",
    latitude: str = "latitude",
    id_column: Optional[str] = None,
) -> str:
    """Convert a Point FeatureCollection to CSV text."""
    if collection.get("type") != "FeatureCollection":
        raise CSVGeoJSONError("expected a FeatureCollection")

    property_names = []
    for feature in collection.get("features", []):
        geometry = feature.get("geometry") or {}
        if geometry.get("type") != "Point":
            raise CSVGeoJSONError("CSV export supports Point features only")
        for key in (feature.get("properties") or {}):
            if key not in property_names:
                property_names.append(key)

    columns = [longitude, latitude]
    if id_column:
        columns.append(id_column)
    columns.extend(property_names)

    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=columns)
    writer.writeheader()
    for feature in collection.get("features", []):
        coordinates = feature["geometry"]["coordinates"]
        row = {
            longitude: coordinates[0],
            latitude: coordinates[1],
        }
        if id_column:
            row[id_column] = feature.get("id", "")
        row.update(feature.get("properties") or {})
        writer.writerow(row)
    return output.getvalue()
