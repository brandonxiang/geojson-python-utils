# geojson-python-utils

Python utilities for working with GeoJSON dictionaries. The package covers common geometry checks, distance calculations, polygon helpers, coordinate conversion, FeatureCollection utilities, and point-line simplification.

The project began as a Python port inspired by [geojson-js-utils](https://github.com/maxogden/geojson-js-utils). It now targets Python 3.8+ and ships inline type annotations.

## Why This Package

- Works with plain Python dictionaries that follow the GeoJSON shape.
- Keeps dependencies small; `requests` is only used by the optional geocoding helper.
- Includes typed public functions and a `py.typed` marker for downstream type checkers.
- Provides tested helpers for common GIS tasks without requiring a full geospatial stack.

## Features

- LineString intersection detection.
- Point-in-Polygon and Point-in-MultiPolygon checks.
- Circle polygon generation from a center point and radius.
- Polygon area, centroid, and rectangle centroid helpers.
- Spherical and ellipsoidal distance calculations.
- Radius checks for Point, LineString, and Polygon geometries.
- Destination point calculation from bearing and distance.
- FeatureCollection merging and endpoint extraction.
- Point array simplification with a meter-based tolerance.
- Coordinate conversion between WGS84, GCJ-02, and BD-09.
- Validation and normalization helpers for GeoJSON geometries, Features, and FeatureCollections.

## Requirements

- Python 3.8 or newer.
- `requests>=2.9.1`.

Python 2 is not supported.

## Installation

```bash
pip install geojson_utils
```

You can also copy the `geojson_utils/` package into a project and import from it directly.

## Quick Start

```python
from geojson_utils import point_distance, point_in_polygon

point = {"type": "Point", "coordinates": [5, 5]}
polygon = {
    "type": "Polygon",
    "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10]]],
}

print(point_in_polygon(point, polygon))

oakland = {"type": "Point", "coordinates": [-122.260000705719, 37.80919060818706]}
naval_base = {"type": "Point", "coordinates": [-122.32083320617676, 37.78774223089045]}

print(point_distance(oakland, naval_base))
```

Most functions accept and return plain GeoJSON dictionaries. The package does not require custom geometry classes.

## Validation and Normalization

```python
from geojson_utils import normalize_geojson, validate_geojson

polygon = {
    "type": "Polygon",
    "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10]]],
}

normalized = normalize_geojson(polygon, close_rings=True)
validate_geojson(normalized)
```

`validate_geojson()` supports every standard GeoJSON geometry type plus Feature and FeatureCollection objects. Invalid objects raise `GeoJSONValidationError` with a path to the failing field.

`normalize_geojson()` returns a copy. It can close polygon rings, orient exterior rings and holes, and optionally remove `bbox` or `id` fields.

## Geometry Helpers

### LineString Intersection

```python
from geojson_utils import linestrings_intersect

diagonal_up = {"type": "LineString", "coordinates": [[0, 0], [10, 10]]}
diagonal_down = {"type": "LineString", "coordinates": [[10, 0], [0, 10]]}
far_away = {"type": "LineString", "coordinates": [[100, 100], [110, 110]]}

print(linestrings_intersect(diagonal_up, diagonal_down))
print(linestrings_intersect(diagonal_up, far_away))
```

### Point in Polygon

```python
from geojson_utils import point_in_multipolygon, point_in_polygon

point = {"type": "Point", "coordinates": [5, 5]}
polygon = {
    "type": "Polygon",
    "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10]]],
}

print(point_in_polygon(point, polygon))

multi_polygon = {
    "type": "MultiPolygon",
    "coordinates": [
        [[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]],
        [[[10, 10], [10, 20], [20, 20], [20, 10], [10, 10]]],
    ],
}

print(point_in_multipolygon(point, multi_polygon))
```

Polygon holes are not handled yet.

### Draw a Circle Polygon

```python
from geojson_utils import draw_circle

center = {"type": "Point", "coordinates": [0, 0]}
circle = draw_circle(10, center, steps=50)

print(circle["type"])
print(len(circle["coordinates"][0]))
```

### Distance and Radius Checks

```python
from geojson_utils import geometry_within_radius, point_distance

center = {"type": "Point", "coordinates": [-122.260000705719, 37.80919060818706]}
candidate = {"type": "Point", "coordinates": [-122.32083320617676, 37.78774223089045]}

print(point_distance(center, candidate))
print(geometry_within_radius(candidate, center, 5853))
```

### Area and Centroid

```python
from geojson_utils import area, centroid, rectangle_centroid

polygon = {
    "type": "Polygon",
    "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10]]],
}

print(area(polygon))
print(centroid(polygon))
print(rectangle_centroid(polygon))
```

### Destination Point

```python
from geojson_utils import destination_point

start = {"type": "Point", "coordinates": [-122.260000705719, 37.80919060818706]}

print(destination_point(start, 180, 2000))
```

## FeatureCollection Helpers

```python
from geojson_utils import merge_featurecollection, simplify_other

merged = merge_featurecollection(first_feature_collection, second_feature_collection)
deduped = simplify_other(major_points, minor_points, dist=50)
```

`simplify_other()` works on Point FeatureCollections. It appends points from the minor collection only when they are farther than `dist` meters from every point in the major collection.

## Simplify Point Arrays

`simplify()` reduces a list of GeoJSON Point objects with the Ramer-Douglas-Peucker algorithm. The `kink` value is measured in meters.

```python
from geojson_utils import simplify

points = [
    {"type": "Point", "coordinates": [0, 0]},
    {"type": "Point", "coordinates": [0.001, 0.00001]},
    {"type": "Point", "coordinates": [0.002, 0]},
]

print(simplify(points, kink=20))
```

The function preserves the first and last point and keeps intermediate points whose perpendicular distance is greater than the `kink` tolerance.

## Coordinate Conversion

`convertor()` supports Geometry, Feature, FeatureCollection, and GeometryCollection inputs. It mutates the input by default for backwards compatibility; pass `inplace=False` to return a converted copy.

| Method | Conversion |
| --- | --- |
| `wgs2gcj` | WGS84 to GCJ-02 |
| `gcj2wgs` | GCJ-02 to WGS84 |
| `wgs2bd` | WGS84 to BD-09 |
| `bd2wgs` | BD-09 to WGS84 |
| `gcj2bd` | GCJ-02 to BD-09 |
| `bd2gcj` | BD-09 to GCJ-02 |

```python
import json

from geojson_utils import convertor

with open("tests/province_wgs.geojson", encoding="utf-8") as fp:
    geojson = json.load(fp)

for feature in geojson["features"]:
converted = convertor(feature["geometry"], method="wgs2gcj")
print(converted["type"])
```

```python
converted = convertor(geojson, method="gcj2bd", inplace=False)
```

The coordinate-transform layer keeps the base install lightweight. EPSG/projection based transforms can be added later behind an optional extra such as `geojson_utils[crs]`.

## Format Conversion API

The conversion layer provides a small registry so the package can grow new adapters without a large monolithic conversion function.

```python
from geojson_utils import convert, read_geojson, write_geojson

point = read_geojson("point.geojson")
text = convert(point, from_format="geojson", to_format="json")
round_tripped = convert(text, from_format="json", to_format="geojson")
write_geojson(round_tripped, "round-trip.geojson")
```

You can add adapters with `register_converter(from_format, to_format, callable)`. Built-in adapters currently cover GeoJSON file IO and GeoJSON dictionary <-> JSON text conversion.

### WKT / WKB

```python
from geojson_utils import geojson_to_wkt, wkt_to_geojson

wkt = geojson_to_wkt({"type": "Point", "coordinates": [1, 2]})
geometry = wkt_to_geojson("POINT (1 2)")
```

WKT support is implemented for standard GeoJSON geometry types. WKB helpers are available through optional Shapely support and raise a clear error when Shapely is not installed.

### CSV Points

```python
from geojson_utils import csv_to_feature_collection, feature_collection_to_csv

collection = csv_to_feature_collection(
    "id,longitude,latitude,name\n1,120.1,30.2,Hangzhou\n",
    id_column="id",
)
text = feature_collection_to_csv(collection, id_column="id")
```

CSV conversion targets Point FeatureCollections. Coordinate columns default to `longitude` and `latitude`, and all other columns are preserved as Feature properties.

## Command Line

Installing the package exposes `geojson-utils` for common pipeline tasks.

```bash
geojson-utils validate input.geojson
geojson-utils convert input.geojson --to json --output output.json
geojson-utils transform input.geojson --method wgs2gcj --output gcj.geojson
geojson-utils simplify line.geojson --tolerance 20 --output simplified.geojson
geojson-utils bbox input.geojson
```

Use `-` as the input path to read GeoJSON from stdin. Commands write to stdout unless `--output` is provided.

## Type Checking

The package includes inline annotations and a `py.typed` marker. Type checkers can read the installed package signatures without separate stub files.

## Development

The active development branch is `develop`.

Run the test suite:

```bash
python3 -m unittest discover -v
```

Run a syntax check:

```bash
python3 -m py_compile geojson_utils/*.py test.py setup.py
```

## Documentation

- [Chinese README](README_CN.md)

## License

[MIT](LICENSE)
