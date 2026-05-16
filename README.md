# geojson-python-utils

Python helper functions for common GeoJSON geometry tasks: intersection checks, point-in-polygon tests, distance calculations, polygon metrics, coordinate conversion, feature collection merging, and point simplification.

This project started as a Python port inspired by [geojson-js-utils](https://github.com/maxogden/geojson-js-utils).

## Features

- LineString intersection detection
- Point-in-Polygon and Point-in-MultiPolygon checks
- Circle polygon generation from a center point and radius
- Polygon area and centroid helpers
- Spherical and ellipsoidal point distance calculations
- Radius checks for Point, LineString, and Polygon geometries
- Destination point calculation from bearing and distance
- FeatureCollection merging and endpoint helpers
- Point-array simplification with a meter-based tolerance
- Coordinate conversion between WGS84, GCJ-02, and BD-09

## Installation

```bash
pip install geojson_utils
```

You can also copy the `geojson_utils/` package into a project and import from it directly.

## Quick Start

```python
from geojson_utils import point_in_polygon, point_distance

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

All functions accept plain Python dictionaries shaped like GeoJSON objects. Most helpers return plain GeoJSON dictionaries as well.

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
from geojson_utils import point_in_polygon, point_in_multipolygon

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

Polygon holes are not handled yet. See the inline TODOs in `geojson_utils/geojson_utils.py`.

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

`simplify_other()` works on Point FeatureCollections. It appends points from the minor collection only when they are farther than `dist` meters from all points in the major collection.

## Simplify Point Arrays

`simplify()` reduces an array of GeoJSON Point objects using a meter-based tolerance.

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

`convertor()` mutates the input geometry and returns it.

Supported conversion methods:

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

## Development

The active development branch is `develop`.

Run the test suite:

```bash
python3 -m unittest discover -v
```

Run a syntax check:

```bash
python3 -m py_compile geojson_utils/*.py test.py
```

## Documentation

- [中文文档](README_CN.md)
- [TODO](TODO.md)

## License

[MIT](LICENSE)
