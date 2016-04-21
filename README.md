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
###point_in_polygon

valid whether the point is located in a polygon

Keyword arguments:

- point -- point geojson object

- poly  -- polygon geojson object

if(point inside poly) return true else false