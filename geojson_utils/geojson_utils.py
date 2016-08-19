import math


def linestrings_intersect(line1, line2):
    """
    To valid whether linestrings from geojson are intersected with each other.
    reference: http://www.kevlindev.com/gui/math/intersection/Intersection.js

    Keyword arguments:
    line1 -- first line geojson object
    line2 -- second line geojson object

    if(line1 intersects with other) return intersect point array else empty array
    """
    intersects = []
    for i in range(0, len(line1['coordinates']) - 1):
        for j in range(0, len(line2['coordinates']) - 1):
            a1_x = line1['coordinates'][i][1]
            a1_y = line1['coordinates'][i][0]
            a2_x = line1['coordinates'][i + 1][1]
            a2_y = line1['coordinates'][i + 1][0]
            b1_x = line2['coordinates'][j][1]
            b1_y = line2['coordinates'][j][0]
            b2_x = line2['coordinates'][j + 1][1]
            b2_y = line2['coordinates'][j + 1][0]
            ua_t = (b2_x - b1_x) * (a1_y - b1_y) - \
                (b2_y - b1_y) * (a1_x - b1_x)
            ub_t = (a2_x - a1_x) * (a1_y - b1_y) - \
                (a2_y - a1_y) * (a1_x - b1_x)
            u_b = (b2_y - b1_y) * (a2_x - a1_x) - (b2_x - b1_x) * (a2_y - a1_y)
            if not u_b == 0:
                u_a = ua_t / u_b
                u_b = ub_t / u_b
                if 0 <= u_a and u_a <= 1 and 0 <= u_b and u_b <= 1:
                    intersects.append({'type': 'Point', 'coordinates': [
                                      a1_x + u_a * (a2_x - a1_x), a1_y + u_a * (a2_y - a1_y)]})
    # if len(intersects) == 0:
    #     intersects = False
    return intersects


def _bbox_around_polycoords(coords):
    """
    bounding box
    """
    x_all = []
    y_all = []

    for first in coords[0]:
        x_all.append(first[1])
        y_all.append(first[0])

    return [min(x_all), min(y_all), max(x_all), max(y_all)]


def _point_in_bbox(point, bounds):
    """
    valid whether the point is inside the bounding box
    """
    return not(point['coordinates'][1] < bounds[0] or point['coordinates'][1] > bounds[2]
               or point['coordinates'][0] < bounds[1] or point['coordinates'][0] > bounds[3])


def _pnpoly(x, y, coords):
    """
    the algorithm to judge whether the point is located in polygon
    reference: https://www.ecse.rpi.edu/~wrf/Research/Short_Notes/pnpoly.html#Explanation
    """
    vert = [[0, 0]]

    for coord in coords:
        for node in coord:
            vert.append(node)
        vert.append(coord[0])
        vert.append([0, 0])

    inside = False

    i = 0
    j = len(vert) - 1

    while i < len(vert):
        if ((vert[i][0] > y) != (vert[j][0] > y)) and (x < (vert[j][1] - vert[i][1])
                                                       * (y - vert[i][0]) / (vert[j][0] - vert[i][0]) + vert[i][1]):
            inside = not inside
        j = i
        i += 1

    return inside


def _point_in_polygon(point, coords):
    inside_box = False
    for coord in coords:
        if inside_box:
            break
        if _point_in_bbox(point, _bbox_around_polycoords(coord)):
            inside_box = True
    if not inside_box:
        return False

    inside_poly = False
    for coord in coords:
        if inside_poly:
            break
        if _pnpoly(point['coordinates'][1], point['coordinates'][0], coord):
            inside_poly = True
    return inside_poly


def point_in_polygon(point, poly):
    """
    valid whether the point is located in a polygon

    Keyword arguments:
    point -- point geojson object
    poly  -- polygon geojson object

    if(point inside poly) return true else false
    """
    coords = [poly['coordinates']] if poly[
        'type'] == 'Polygon' else poly['coordinates']
    return _point_in_polygon(point, coords)


def point_in_multipolygon(point, multipoly):
    """
    valid whether the point is located in a mulitpolygon (donut polygon is not supported)

    Keyword arguments:
    point      -- point geojson object
    multipoly  -- multipolygon geojson object

    if(point inside multipoly) return true else false
    """
    coords_array = [multipoly['coordinates']] if multipoly[
        'type'] == "MultiPolygon" else multipoly['coordinates']

    for coords in coords_array:
        if _point_in_polygon(point, coords):
            return True

    return False


def number2radius(number):
    """
    convert degree into radius

    Keyword arguments:
    number -- degree

    return radius
    """
    return number * math.pi / 180


def number2degree(number):
    """
    convert radius into degree

    Keyword arguments:
    number -- radius

    return degree
    """
    return number * 180 / math.pi


def draw_circle(radius_in_meters, center_point, steps=15):
    """
    get a circle shape polygon based on centerPoint and radius

    Keyword arguments:
    point1  -- point one geojson object
    point2  -- point two geojson object

    if(point inside multipoly) return true else false
    """
    steps = steps if steps > 15 else 15
    center = [center_point['coordinates'][1], center_point['coordinates'][0]]
    dist = (radius_in_meters / 1000) / 6371
    # convert meters to radiant
    rad_center = [number2radius(center[0]), number2radius(center[1])]
    # 15 sided circle
    poly = []
    for step in range(0, steps):
        brng = 2 * math.pi * step / steps
        lat = math.asin(math.sin(rad_center[0]) * math.cos(dist) +
                        math.cos(rad_center[0]) * math.sin(dist) * math.cos(brng))
        lng = rad_center[1] + math.atan2(math.sin(brng) * math.sin(dist)
                                         * math.cos(rad_center[0]), math.cos(dist) - math.sin(rad_center[0]) * math.sin(lat))
        poly.append([number2degree(lng), number2degree(lat)])
    return {"type": "Polygon", "coordinates": [poly]}


def rectangle_centroid(rectangle):
    """
    get the centroid of the rectangle

    Keyword arguments:
    rectangle  -- polygon geojson object

    return centroid
    """
    bbox = rectangle['coordinates'][0]
    xmin = bbox[0][0]
    ymin = bbox[0][1]
    xmax = bbox[2][0]
    ymax = bbox[2][1]
    xwidth = xmax - xmin
    ywidth = ymax - ymin
    return {'type': 'Point', 'coordinates': [xmin + xwidth / 2, ymin + ywidth / 2]}


def point_distance(point1, point2):
    """
    calculate the distance between two points on the sphere like google map
    reference http://www.movable-type.co.uk/scripts/latlong.html

    Keyword arguments:
    point1  -- point one geojson object
    point2  -- point two geojson object

    return distance
    """
    lon1 = point1['coordinates'][0]
    lat1 = point1['coordinates'][1]
    lon2 = point2['coordinates'][0]
    lat2 = point2['coordinates'][1]
    deg_lat = number2radius(lat2 - lat1)
    deg_lon = number2radius(lon2 - lon1)
    a = math.pow(math.sin(deg_lat / 2), 2) + math.cos(number2radius(lat1)) * \
        math.cos(number2radius(lat2)) * math.pow(math.sin(deg_lon / 2), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return (6371 * c) * 1000
    
def point_distance_ellipsode(point1,point2):
    """
    calculate the distance between two points on the ellipsode based on point1
    
    Keyword arguments:
    point1  -- point one geojson object
    point2  -- point two geojson object
    
    return distance
    """
    a = 6378137
    f = 1/298.25722
    b = a - a*f
    e = math.sqrt((a*a-b*b)/(a*a))
    lon1 = point1['coordinates'][0]
    lat1 = point1['coordinates'][1]
    lon2 = point1['coordinates'][0]
    lat2 = point2['coordinates'][1]
    M = a*(1-e*e)*math.pow(1-math.pow(e*math.sin(number2radius(lat1)),2),-1.5)
    N = a/(math.pow(1-math.pow(e*math.sin(number2radius(lat1)),2),0.5))
    
    distance_lat = M*number2radius(lat2-lat1)
    distance_lon = N*math.cos(number2radius(lat1))*(lon2-lon1)*3600*math.sin(1/3600*math.pi/180)
    return math.sqrt(distance_lat*distance_lat+distance_lon*distance_lon)


def geometry_within_radius(geometry, center, radius):
    """
    To valid whether point or linestring or polygon is inside a radius around a center

    Keyword arguments:
    geometry  -- point/linstring/polygon geojson object
    center    -- point geojson object
    radius    -- radius

    if(geometry inside radius) return true else false
    """
    if geometry['type'] == 'Point':
        return point_distance(geometry, center) <= radius
    elif geometry['type'] == 'LineString' or geometry['type'] == 'Polygon':
        point = {}
        # it's enough to check the exterior ring of the Polygon
        coordinates = geometry['coordinates'][0] if geometry['type'] == 'Polygon' else geometry['coordinates']

        for coordinate in coordinates:
            point['coordinates'] = coordinate
            if point_distance(point, center) > radius:
                return False
    return True


def area(poly):
    """
    calculate the area of polygon

    Keyword arguments:
    poly -- polygon geojson object

    return polygon area
    """
    poly_area = 0
    # TODO: polygon holes at coordinates[1]
    points = poly['coordinates'][0]
    j = len(points) - 1
    count = len(points)

    for i in range(0, count):
        p1_x = points[i][1]
        p1_y = points[i][0]
        p2_x = points[j][1]
        p2_y = points[j][0]

        poly_area += p1_x * p2_y
        poly_area -= p1_y * p2_x
        j = i

    poly_area /= 2
    return poly_area


def centroid(poly):
    """
    get the centroid of polygon
    adapted from http://paulbourke.net/geometry/polyarea/javascript.txt

    Keyword arguments:
    poly -- polygon geojson object

    return polygon centroid
    """
    f_total = 0
    x_total = 0
    y_total = 0
    # TODO: polygon holes at coordinates[1]
    points = poly['coordinates'][0]
    j = len(points) - 1
    count = len(points)

    for i in range(0, count):
        p1_x = points[i][1]
        p1_y = points[i][0]
        p2_x = points[j][1]
        p2_y = points[j][0]

        f_total = p1_x * p2_y - p2_x * p1_y
        x_total += (p1_x + p2_x) * f_total
        y_total += (p1_y + p2_y) * f_total
        j = i

    six_area = area(poly) * 6
    return {'type': 'Point', 'coordinates': [y_total / six_area, x_total / six_area]}


def destination_point(point, brng, dist):
    """
    Calculate a destination Point base on a base point and a distance

    Keyword arguments:
    pt   -- polygon geojson object
    brng -- an angle in degrees
    dist -- distance in Kilometer between destination and base point

    return destination point object

    """
    dist = float(dist) / 6371  # convert dist to angular distance in radians
    brng = number2radius(brng)

    lon1 = number2radius(point['coordinates'][0])
    lat1 = number2radius(point['coordinates'][1])

    lat2 = math.asin(math.sin(lat1) * math.cos(dist) +
                     math.cos(lat1) * math.sin(dist) * math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(dist) *
                             math.cos(lat1), math.cos(dist) - math.sin(lat1) * math.sin(lat2))
    lon2 = (lon2 + 3 * math.pi) % (2 * math.pi) - math.pi  # normalise to -180 degree +180 degree

    return {'type': 'Point', 'coordinates': [number2degree(lon2), number2degree(lat2)]}


def simplify(source, kink=20):
    """
     source[] array of geojson points
     kink	in metres, kinks above this depth kept
     kink depth is the height of the triangle abc where a-b and b-c are two consecutive line segments
    """
    source_coord = map(lambda o: {"lng": o.coordinates[0], "lat": o.coordinates[1]}, source)

    # count, n_stack, n_dest, start, end, i, sig;
    # dev_sqr, max_dev_sqr, band_sqr;
    # x12, y12, d12, x13, y13, d13, x23, y23, d23;
    F = (math.pi / 180.0) * 0.5
    index = [] # aray of indexes of source points to include in the reduced line
    sig_start = [] # indices of start & end of working section
    sig_end = []

    # check for simple cases
    count = len(source_coord)
    if count < 3:
        return source_coord # one or two points

    # more complex case. initialize stack

    band_sqr = kink * 360.0 / (2.0 * math.pi * 6378137.0) # Now in degrees
    band_sqr *= band_sqr
    n_dest = 0
    sig_start[0] = 0
    sig_end[0] = count - 1
    n_stack = 1

    # while the stack is not empty
    while n_stack > 0:
        # ... pop the top-most entries off the stacks
        start = sig_start[n_stack - 1]
        end = sig_end[n_stack - 1]
        n_stack -= 1

        if (end - start) > 1: #any intermediate points ?
            # ... yes, so find most deviant intermediate point to either side of line joining start & end points
            x12 = source[end]["lng"] - source[start]["lng"]
            y12 = source[end]["lat"] - source[start]["lat"]
            if math.fabs(x12) > 180.0:
                x12 = 360.0 - math.fabs(x12)
            x12 *= math.cos(F * (source[end]["lat"] + source[start]["lat"])) # use avg lat to reduce lng
            d12 = (x12 * x12) + (y12 * y12)

            i = start + 1
            sig = start
            max_dev_sqr = -1.0
            while i < end:
                x13 = source[i]["lng"] - source[start]["lng"]
                y13 = source[i]["lat"] - source[start]["lat"]
                if math.fabs(x13) > 180.0:
                    x13 = 360.0 - math.fabs(x13)
                x13 *= math.cos(F * (source[i]["lat"] + source[start]["lat"]))
                d13 = (x13 * x13) + (y13 * y13)
                x23 = source[i]["lng"] - source[end]["lng"]
                y23 = source[i]["lat"] - source[end]["lat"]
                if math.fabs(x23) > 180.0:
                    x23 = 360.0 - math.fabs(x23)
                x23 *= math.cos(F * (source[i]["lat"] + source[end]["lat"]))
                d23 = (x23 * x23) + (y23 * y23)

                if d13 >= (d12 + d23):
                    dev_sqr = d23
                elif d23 >= (d12 + d13):
                    dev_sqr = d13
                else:
                    dev_sqr = (x13 * y12 - y13 * x12) * (x13 * y12 - y13 * x12) / d12 # solve triangle
                if dev_sqr > max_dev_sqr:
                    sig = i
                    max_dev_sqr = dev_sqr
                i += 1


            if max_dev_sqr < band_sqr: # is there a sig. intermediate point ?
            #... no, so transfer current start point
                index[n_dest] = start
                n_dest += 1
            else: # ... yes, so push two sub-sections on stack for further processing
                n_stack += 1
                sig_start[n_stack - 1] = sig
                sig_end[n_stack - 1] = end
                n_stack += 1
                sig_start[n_stack - 1] = start
                sig_end[n_stack - 1] = sig

        else:  # ... no intermediate points, so transfer current start point
            index[n_dest] = start
            n_dest += 1

    # transfer last point
    index[n_dest] = count - 1
    n_dest += 1

    # make return array
    r = []
    for i in range(0, n_dest):
        r.append(source_coord[index[i]])

    return map(lambda o:  {"type": "Point","coordinates": [o.lng, o.lat]}, r)




