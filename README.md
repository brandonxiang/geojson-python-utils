# geojson-python-utils

This project is inspired by [geojson-js-utils](https://github.com/maxogden/geojson-js-utils). Geojson becomes more popular than before. These algorithms also are what I want to learn about, which may give you some inspiration.

****
###linestrings intersect

To valid whether linestrings from geojson are intersected with each other.

Keyword arguments:

- line1 -- first line geojson object
- line2 -- second line geojson object

if(line1 intersects with other) return intersect point array else empty array

****
###point in polygon
valid whether the point is located in a polygon

Keyword arguments:

- point -- point geojson object
- poly  -- polygon geojson object

if(point inside poly) return true else false

****
###point in multipolygon
valid whether the point is located in a mulitpolygon (donut polygon is not supported)

Keyword arguments:

- point      -- point geojson object
- multipoly  -- multipolygon geojson object

if(point inside multipoly) return true else false

***
### draw circle
get a circle shape polygon based on centerPoint and radius

Keyword arguments:
- point1  -- point one geojson object
- point2  -- point two geojson object

if(point inside multipoly) return true else false

****
### rectangle centroid
get the centroid of the rectangle

Keyword arguments:
- rectangle  -- polygon geojson object

return centroid
  

****
### point distance
calculate the distance between two point on the sphere like google map
reference http://www.movable-type.co.uk/scripts/latlong.html

Keyword arguments:
- point1  -- point one geojson object
- point2  -- point two geojson object

if(point inside multipoly) return true else false


****
###geometry within radius
valid whether point or linestring or polygon is inside a radius around a center

Keyword arguments:
- geometry  -- point geojson object
- center    -- linestring geojson object
- radius    -- polygon geojson object

if(geometry inside radius) return true else false
