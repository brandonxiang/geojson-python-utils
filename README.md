# geojson-python-utils

> JavaScript Version: [geojson-js-utils](https://github.com/maxogden/geojson-js-utils)

This project is inspired by [geojson-js-utils](https://github.com/maxogden/geojson-js-utils). Geojson becomes more popular than before. These algorithms also are what I want to learn about, which may give you some inspiration.

## Chinese Doc

[中文文档](README_CN.md)

## Usage

Copy `geojson_utils.py` into your working directory, and import the modules into your py file.

```
from geojson_utils import linestrings_intersect
```

or install

```
pip install geojson_utils
```

## Example

### Linestrings Intersection

To valid whether linestrings from geojson are intersected with each other.

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

### Point in Polygon
To valid whether the point is located in a polygon

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


### Point in Multipolygon
To valid whether the point is located in a mulitpolygon (donut polygon is not supported)

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


### Draw Circle
To get a circle shape polygon based on centerPoint and radius

```
from geojson_utils import draw_circle

pt_center = json.loads('{"type": "Point", "coordinates": [0, 0]}')

print len(draw_circle(10, pt_center)['coordinates'][0])
#15
print len(draw_circle(10, pt_center, 50)['coordinates'][0])
#50
```


### Rectangle Centroid
To get the centroid of the rectangle

```
from geojson_utils import centroid

box_str = '{"type": "Polygon","coordinates": [[[0, 0],[10, 0],[10, 10],[0, 10]]]}'
box = json.loads(box_str)
centroid = rectangle_centroid(box)

print centroid['coordinates']
#[5, 5]
```
  


### Distance between Two Points
To calculate the distance between two point on the sphere like google map (reference http://www.movable-type.co.uk/scripts/latlong.html)

```
from geojson_utils import point_distance

fairyland_str = '{"type": "Point", "coordinates": [-122.260000705719, 37.80919060818706]}'
navalbase_str = '{"type": "Point", "coordinates": [-122.32083320617676, 37.78774223089045]}'
fairyland = json.loads(fairyland_str)
navalbase = json.loads(navalbase_str)

print math.floor(point_distance(fairyland, navalbase))
# 5852
```



### Geometry within Radius
To valid whether point or linestring or polygon is inside a radius around a center

```
from geojson_utils import geometry_within_radius

center_point_str = '{"type": "Point", "coordinates":  [-122.260000705719, 37.80919060818706]}'
check_point_str = '{"type": "Point", "coordinates": [-122.32083320617676, 37.78774223089045]}'
center_point = json.loads(center_point_str)
check_point = json.loads(check_point_str)

print geometry_within_radius(check_point, center_point, 5853)
#True
```


### Area
To calculate the area of polygon

```
from geojson_utils import area
 
box_str = '{"type": "Polygon","coordinates": [[ [0, 0], [10, 0], [10, 10], [0, 10] ]]}'
box = json.loads(box_str)
print area(box)
#100
```


### Centroid
To get the centroid of polygon
adapted from http://paulbourke.net/geometry/polyarea/javascript.txt

```
from geojson_utils import centroid
box_str = '{"type": "Polygon","coordinates": [[ [0, 0], [10, 0], [10, 10], [0, 10] ]]}'
box = json.loads(box_str)

print centroid(box)
#{"type": "Point", "coordinates": [5, 5]})
```


### Destination point
To calculate a destination Point base on a base point and a distance

```
from geojson_utils import destination_point

startpoint_str = '{"type": "Point", "coordinates":  [-122.260000705719, 37.80919060818706]}'
startpoint = json.loads(startpoint_str)

print destination_point(startpoint, 180, 2000)
#{'type': 'Point', 'coordinates': [-122.26000070571902, 19.822758489812447]}
```

### Merge Featurecollection geojson 

To merge features into one featurecollection

```
from geojson_utils import merge_featurecollection
with open('tests/first.json','r') as fp:
    first = json.load(fp)
with open('tests/second.json','r') as fp:
    second = json.load(fp)
with open('tests/result.json','r') as fp:
    result = json.load(fp)
merge_featurecollection(first,second)
```

### Simplify other point

Simplify the point featurecollection of poi with another point features accoording by distance.

Attention: point featurecollection only

## Conversion between wgs84, gcj02, bd09

Conversion between wgs84, gcj02 and bd09

Parameter One: geojson geometry

Parameter Two: 

- **wgs2gcj** coordinates conversion from wgs84 to gcj02  
- **gcj2wgs** coordinates conversion from gcj02 to wgs84 
- **wgs2bd** coordinates conversion from wgs84 to bd09 
- **bd2wgs** coordinates conversion from bd09 to wgs84 
- **gcj2bd** coordinates conversion from gcj02 to bd09 
- **bd2gcj** coordinates conversion from bd09 to gcj02 


```
from geojson_utils import convertor
with open('tests/province_wgs.geojson', encoding='utf-8') as fp:
    geojson = json.load(fp)
    features = geojson['features']
    for feature in features:
        origin = feature['geometry']['coordinates'][0][0][0]
        result = convertor(feature['geometry'])
```


## TODO

[TODO](TODO,md)

## Development 

On the develop branch

## License

[MIT](LICENSE)
