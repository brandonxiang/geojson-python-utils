# Geojson笔记二：geojson-python-util

> 源码github地址在此，记得点星：
https://github.com/brandonxiang/geojson-python-utils

> 该项目是geojson-js-util的python实现

随着geojson变得越来越流行，需要给geojson一些具体的数据操作。我在写这段库的工程中也是学习的过程，希望也能给你的GIS学习一点点帮助。

## 英文文档

[English DOC](README.md)

## 使用方法

将脚本`geojson_utils.py`复制到你的文件夹中，然后输入：

```
from geojson_utils import linestrings_intersect
```

## 例子

###Linestrings Intersection（两线的交点）
验证两条线是否相交并求出交点。[原理]( http://www.kevlindev.com/gui/math/intersection/Intersection.js)

```
from geojson_utils import linestrings_intersect

diagonal_up_str = '{ "type": "LineString","coordinates": [[0, 0], [10, 10]]}'
diagonal_down_str = '{ "type": "LineString","coordinates": [[10, 0], [0, 10]]}'
far_away_str = '{ "type": "LineString","coordinates": [[100, 100], [110, 110]]}'
diagonal_up = json.loads(diagonal_up_str)
diagonal_down = json.loads(diagonal_down_str)
far_away = json.loads(far_away_str)

print linestrings_intersect(diagonal_up, diagonal_down)
#[{'type': 'Point', 'coordinates': [0, 0]}]
print linestrings_intersect(diagonal_up, far_away)
#[]
```

### Point in Polygon（点是否在多边形内）
判断点是否在多边形内部。原理大致如下：
- 先找到多边形的外包矩形
- 判断点是否在外包矩形内部，不在则排除在外，在则继续判断
- 算法计算点是否在多边形内，[原理](https://www.ecse.rpi.edu/~wrf/Research/Short_Notes/pnpoly.html#Explanation)

```
from geojson_utils import point_in_polygon

in_str = '{"type": "Point", "coordinates": [5, 5]}'
out_str = '{"type": "Point", "coordinates": [15, 15]}'
box_str = '{"type": "Polygon","coordinates": [[ [0, 0], [10, 0], [10, 10], [0, 10] ]]}'
in_box = json.loads(in_str)
out_box = json.loads(out_str)
box = json.loads(box_str)

print point_in_polygon(in_box, box)
#True
point_in_polygon(out_box, box)
#False
```


### Point in Multipolygon（点是否在多个多边形内）
判断点是否在多个多边形内

```
from geojson_utils import point_in_multipolygon

point_str = '{"type": "Point", "coordinates": [0.5, 0.5]}'
single_point_str = '{"type": "Point", "coordinates": [-1, -1]}'
multipoly_str = '{"type":"MultiPolygon","coordinates":[[[[0,0],[0,10],[10,10],[10,0],[0,0]]],[[[10,10],[10,20],[20,20],[20,10],[10,10]]]]}'
point = json.loads(point_str)
single_point = json.loads(single_point_str)
multipoly = json.loads(multipoly_str)

print point_in_multipolygon(point, multipoly)
#True
print point_in_multipolygon(single_point, multipoly)
#False
```


### Draw Circle（画圆）
通过一个中心点和半径获得一个圆形的图形

```
from geojson_utils import draw_circle

pt_center = json.loads('{"type": "Point", "coordinates": [0, 0]}')

print len(draw_circle(10, pt_center)['coordinates'][0])
#15
print len(draw_circle(10, pt_center, 50)['coordinates'][0])
#50
```


### Rectangle Centroid（矩形的中心点）
取出矩形的中心点

```
from geojson_utils import centroid

box_str = '{"type": "Polygon","coordinates": [[[0, 0],[10, 0],[10, 10],[0, 10]]]}'
box = json.loads(box_str)
centroid = rectangle_centroid(box)

print centroid['coordinates']
#[5, 5]
```
 
### Distance between Two Points（两个点的大地距离）
两点的互联网球面距离
(参考 http://www.movable-type.co.uk/scripts/latlong.html)，注意这个是球型距离，非大地陀球距离

```
from geojson_utils import point_distance

fairyland_str = '{"type": "Point", "coordinates": [-122.260000705719, 37.80919060818706]}'
navalbase_str = '{"type": "Point", "coordinates": [-122.32083320617676, 37.78774223089045]}'
fairyland = json.loads(fairyland_str)
navalbase = json.loads(navalbase_str)

print math.floor(point_distance(fairyland, navalbase))
# 5852
```



### Geometry within Radius（几何体在半径内部）
判断点线面是否在某点半价内

```
from geojson_utils import geometry_within_radius

center_point_str = '{"type": "Point", "coordinates":  [-122.260000705719, 37.80919060818706]}'
check_point_str = '{"type": "Point", "coordinates": [-122.32083320617676, 37.78774223089045]}'
center_point = json.loads(center_point_str)
check_point = json.loads(check_point_str)

print geometry_within_radius(check_point, center_point, 5853)
#True
```


### Area（面积）
求多边形面积

```
from geojson_utils import area
 
box_str = '{"type": "Polygon","coordinates": [[ [0, 0], [10, 0], [10, 10], [0, 10] ]]}'
box = json.loads(box_str)
print area(box)
#100
```


### Centroid（中心点）
多边形中心点
adapted from http://paulbourke.net/geometry/polyarea/javascript.txt

```
from geojson_utils import centroid
box_str = '{"type": "Polygon","coordinates": [[ [0, 0], [10, 0], [10, 10], [0, 10] ]]}'
box = json.loads(box_str)

print centroid(box)
#{"type": "Point", "coordinates": [5, 5]})
```


### Destination point（终点）
通过起点，距离和角度来计算终点

```
from geojson_utils import destination_point

startpoint_str = '{"type": "Point", "coordinates":  [-122.260000705719, 37.80919060818706]}'
startpoint = json.loads(startpoint_str)

print destination_point(startpoint, 180, 2000)
#{'type': 'Point', 'coordinates': [-122.26000070571902, 19.822758489812447]}
```

转载，请表明出处。[总目录Awesome GIS](http://www.jianshu.com/p/3b3efa92dd6d)