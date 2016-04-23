# geojson-python-utils

This project is inspired by [geojson-js-utils](https://github.com/maxogden/geojson-js-utils). Geojson becomes more popular than before. These algorithms also are what I want to learn about, which may give you some inspiration.

###Usage

Copy the py file into your working file, and load `geojson_utils` into your py file.

```
from geojson_utils import linestrings_intersect
from geojson_utils import point_in_polygon
from geojson_utils import point_in_multipolygon
from geojson_utils import draw_circle
from geojson_utils import rectangle_centroid
from geojson_utils import point_distance
```


****
###Linestrings Intersection

To valid whether linestrings from geojson are intersected with each other.

Keyword arguments:

- line1 -- first line geojson object
- line2 -- second line geojson object

if(line1 intersects with other) return intersect point array else empty array

****
###Point in Polygon
valid whether the point is located in a polygon

Keyword arguments:

- point -- point geojson object
- poly  -- polygon geojson object

if(point inside poly) return true else false

****
###Point in Multipolygon
valid whether the point is located in a mulitpolygon (donut polygon is not supported)

Keyword arguments:

- point      -- point geojson object
- multipoly  -- multipolygon geojson object

if(point inside multipoly) return true else false

***
### Draw Circle
get a circle shape polygon based on centerPoint and radius

Keyword arguments:
- point1  -- point one geojson object
- point2  -- point two geojson object

if(point inside multipoly) return true else false

****
### Rectangle Centroid
get the centroid of the rectangle

Keyword arguments:
- rectangle  -- polygon geojson object

return centroid
  

****
### Distance between Two Points
calculate the distance between two point on the sphere like google map
reference http://www.movable-type.co.uk/scripts/latlong.html

Keyword arguments:
- point1  -- point one geojson object
- point2  -- point two geojson object

if(point inside multipoly) return true else false


****
###Geometry within Radius
valid whether point or linestring or polygon is inside a radius around a center

Keyword arguments:
- geometry  -- point geojson object
- center    -- linestring geojson object
- radius    -- polygon geojson object

if(geometry inside radius) return true else false

****
###Area
calculate the area of polygon

Keyword arguments:
- poly -- polygon geojson object

return polygon area

****
###Centroid
get the centroid of polygon
adapted from http://paulbourke.net/geometry/polyarea/javascript.txt

Keyword arguments:
poly -- polygon geojson object

return polygon centroid

****
###Destination point

Calculate a destination Point base on a base point and a distance

Keyword arguments:
pt   -- polygon geojson object
brng -- an angle in radius
dist -- distance between destination point and base point 

return destination point object