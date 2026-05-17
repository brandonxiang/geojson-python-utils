# geojson-python-utils

用于处理 GeoJSON 字典数据的 Python 工具包。它覆盖常见的几何判断、距离计算、多边形辅助函数、坐标系转换、FeatureCollection 工具、点线简化、验证规范化、格式转换和命令行处理流程。

项目最初受 [geojson-js-utils](https://github.com/maxogden/geojson-js-utils) 启发，是它的 Python 实现。现在项目面向 Python 3.8+，并内置类型标注。

## 为什么使用这个包

- 直接使用符合 GeoJSON 结构的普通 Python 字典。
- 依赖保持轻量；`requests` 只用于可选的 geocoding 辅助能力。
- 提供类型标注和 `py.typed`，方便下游类型检查器识别。
- 不依赖完整 GIS 技术栈，也能完成常见 GIS 数据处理任务。

## 功能

- LineString 相交检测。
- Point-in-Polygon 和 Point-in-MultiPolygon 判断。
- 根据中心点和半径生成圆形 Polygon。
- Polygon 面积、中心点和矩形中心点辅助函数。
- 球面距离和椭球距离计算。
- Point、LineString、Polygon 的半径范围判断。
- 根据起点、角度和距离计算目标点。
- FeatureCollection 合并和端点提取。
- 基于米级容差的点数组简化。
- WGS84、GCJ-02、BD-09 坐标系互转。
- GeoJSON Geometry、Feature、FeatureCollection 的验证和规范化。
- 可插拔格式转换 API，支持 JSON、WKT、CSV 等格式扩展。
- CLI 命令行工具、NDJSON 流式处理、bbox 和空间过滤工具。

## 环境要求

- Python 3.8 或更新版本。
- `requests>=2.9.1`。

Python 2 不再支持。

## 安装

```bash
pip install geojson_utils
```

也可以直接把 `geojson_utils/` 目录复制到项目中使用。

## 快速开始

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

大部分函数都接收并返回普通 GeoJSON 字典，不需要自定义几何对象。

## 验证和规范化

```python
from geojson_utils import normalize_geojson, validate_geojson

polygon = {
    "type": "Polygon",
    "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10]]],
}

normalized = normalize_geojson(polygon, close_rings=True)
validate_geojson(normalized)
```

`validate_geojson()` 支持所有标准 GeoJSON Geometry 类型，以及 Feature 和 FeatureCollection。非法对象会抛出 `GeoJSONValidationError`，错误信息包含失败字段路径。

`normalize_geojson()` 返回输入对象的副本。它可以自动闭合 polygon ring、调整外环和洞的方向，并可选择移除 `bbox` 或 `id` 字段。

## 几何辅助函数

### LineString 相交

```python
from geojson_utils import linestrings_intersect

diagonal_up = {"type": "LineString", "coordinates": [[0, 0], [10, 10]]}
diagonal_down = {"type": "LineString", "coordinates": [[10, 0], [0, 10]]}
far_away = {"type": "LineString", "coordinates": [[100, 100], [110, 110]]}

print(linestrings_intersect(diagonal_up, diagonal_down))
print(linestrings_intersect(diagonal_up, far_away))
```

### 点是否在多边形内

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

Polygon holes 已用于点面关系、面积和中心点计算。边界点会被视为在面内。

### 生成圆形 Polygon

```python
from geojson_utils import draw_circle

center = {"type": "Point", "coordinates": [0, 0]}
circle = draw_circle(10, center, steps=50)

print(circle["type"])
print(len(circle["coordinates"][0]))
```

### 距离和半径判断

```python
from geojson_utils import geometry_within_radius, point_distance

center = {"type": "Point", "coordinates": [-122.260000705719, 37.80919060818706]}
candidate = {"type": "Point", "coordinates": [-122.32083320617676, 37.78774223089045]}

print(point_distance(center, candidate))
print(geometry_within_radius(candidate, center, 5853))
```

### 面积和中心点

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

导出前可以使用 `close_ring()`、`ring_is_clockwise()` 和 `orient_ring()` 规范化 polygon topology。

### 目标点计算

```python
from geojson_utils import destination_point

start = {"type": "Point", "coordinates": [-122.260000705719, 37.80919060818706]}

print(destination_point(start, 180, 2000))
```

## FeatureCollection 工具

```python
from geojson_utils import merge_featurecollection, simplify_other

merged = merge_featurecollection(first_feature_collection, second_feature_collection)
deduped = simplify_other(major_points, minor_points, dist=50)
```

`simplify_other()` 用于 Point FeatureCollection。只有当 minor collection 中的点距离 major collection 中所有点都大于 `dist` 米时，才会被追加到结果中。

## 点数组简化

`simplify()` 使用 Ramer-Douglas-Peucker 算法简化 GeoJSON Point 对象列表。`kink` 使用米作为单位。

```python
from geojson_utils import simplify

points = [
    {"type": "Point", "coordinates": [0, 0]},
    {"type": "Point", "coordinates": [0.001, 0.00001]},
    {"type": "Point", "coordinates": [0.002, 0]},
]

print(simplify(points, kink=20))
```

函数会保留首尾点，并保留垂直距离大于 `kink` 容差的中间点。

## 坐标转换

`convertor()` 支持 Geometry、Feature、FeatureCollection 和 GeometryCollection。为了兼容旧行为，默认会修改输入对象；传入 `inplace=False` 可以返回转换后的副本。

| 方法 | 转换 |
| --- | --- |
| `wgs2gcj` | WGS84 到 GCJ-02 |
| `gcj2wgs` | GCJ-02 到 WGS84 |
| `wgs2bd` | WGS84 到 BD-09 |
| `bd2wgs` | BD-09 到 WGS84 |
| `gcj2bd` | GCJ-02 到 BD-09 |
| `bd2gcj` | BD-09 到 GCJ-02 |

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

坐标转换层保持轻量。EPSG / projection 转换可以后续通过 `geojson_utils[crs]` 这类可选 extra 接入。

## 格式转换 API

转换层提供一个小型 registry，让后续格式适配器可以独立扩展，而不是塞进一个巨大的转换函数。

```python
from geojson_utils import convert, read_geojson, write_geojson

point = read_geojson("point.geojson")
text = convert(point, from_format="geojson", to_format="json")
round_tripped = convert(text, from_format="json", to_format="geojson")
write_geojson(round_tripped, "round-trip.geojson")
```

可以通过 `register_converter(from_format, to_format, callable)` 注册新的转换器。内置适配器目前覆盖 GeoJSON 文件 IO，以及 GeoJSON 字典和 JSON 文本之间的转换。

### WKT / WKB

```python
from geojson_utils import geojson_to_wkt, wkt_to_geojson

wkt = geojson_to_wkt({"type": "Point", "coordinates": [1, 2]})
geometry = wkt_to_geojson("POINT (1 2)")
```

WKT 支持标准 GeoJSON Geometry 类型。WKB helper 通过可选 Shapely 支持实现；未安装 Shapely 时会抛出清晰错误。

### CSV 点数据

```python
from geojson_utils import csv_to_feature_collection, feature_collection_to_csv

collection = csv_to_feature_collection(
    "id,longitude,latitude,name\n1,120.1,30.2,Hangzhou\n",
    id_column="id",
)
text = feature_collection_to_csv(collection, id_column="id")
```

CSV 转换面向 Point FeatureCollection。坐标列默认是 `longitude` 和 `latitude`，其他列会保留为 Feature properties。

### Shapefile / GeoPackage

桌面 GIS 常见文件格式通过可选适配器暴露，避免基础包变重。

```bash
pip install "geojson_utils[files]"
```

```python
from geojson_utils import read_geopackage, read_shapefile, write_geopackage, write_shapefile

collection = read_shapefile("roads.shp")
write_geopackage(collection, "roads.gpkg", layer="roads")
```

这些适配器在安装 GeoPandas 后可用。未安装可选依赖时，会抛出带安装提示的 `OptionalAdapterError`。

## Streaming 和 NDJSON

处理大数据集时，可以使用 Feature iterator 和 newline-delimited GeoJSON helper，避免一次性把所有 feature 加载到内存中。

```python
from geojson_utils import read_ndjson_features, write_ndjson_features

with open("features.ndjson", encoding="utf-8") as source:
    features = read_ndjson_features(source)
    for feature in features:
        print(feature["geometry"]["type"])
```

`iter_features()` 可以从 Feature、FeatureCollection 或裸 Geometry 中产出 Feature 对象。`write_ndjson_features()` 会每行写入一个 Feature，适合数据管道处理。

## Bounding Box 和空间过滤

```python
from geojson_utils import BBoxIndex, bbox, filter_features_by_bbox

bounds = bbox(collection)
nearby = filter_features_by_bbox(collection, [120, 30, 121, 31])
indexed = BBoxIndex(collection).search([120, 30, 121, 31])
```

`bbox()` 会为 Geometry、Feature 和 FeatureCollection 返回 `[min_lon, min_lat, max_lon, max_lat]`。轻量级 `BBoxIndex` 会缓存 feature bbox，适合重复 bbox 查询，不需要额外 R-tree 依赖。

## 命令行

安装后会提供 `geojson-utils` 命令行工具，用于常见数据处理管线。

```bash
geojson-utils validate input.geojson
geojson-utils convert input.geojson --to json --output output.json
geojson-utils transform input.geojson --method wgs2gcj --output gcj.geojson
geojson-utils simplify line.geojson --tolerance 20 --output simplified.geojson
geojson-utils bbox input.geojson
```

输入路径使用 `-` 时会从 stdin 读取 GeoJSON。未提供 `--output` 时，命令默认输出到 stdout。

## 类型检查

包内包含 inline annotations 和 `py.typed` 标记。类型检查器可以直接读取安装包中的函数签名，不需要额外 stub 文件。

## 开发

当前活跃开发分支是 `develop`。

运行测试：

```bash
python3 -m unittest discover -v
```

运行语法检查：

```bash
python3 -m py_compile geojson_utils/*.py test.py setup.py
```

## 文档

- [English README](README.md)

## License

[MIT](LICENSE)
