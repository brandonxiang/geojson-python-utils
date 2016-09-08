import math
from copy import deepcopy
from geojson import Point,Feature,FeatureCollection
from geojson_utils import point_distance

def merge_featurecollection(*jsons):
    """
    merge features into one featurecollection

    Keyword arguments:
    jsons   -- jsons object list 

    return geojson featurecollection
    """
    features = []
    for json in jsons:
        if json['type'] == 'FeatureCollection':
            for feature in json['features']:
                features.append(feature)
    return {"type":'FeatureCollection', "features":features}

def simplify_other(major, minor, dist):
    """
    Simplify the point featurecollection of poi with another point features accoording by distance.
    Attention: point featurecollection only

    Keyword arguments:
    major    -- major geojson
    minor    -- minor geojson
    dist     -- distance 

    return a geojson featurecollection with two parts of featurecollection
    """
    result = deepcopy(major)
    if major['type'] == 'FeatureCollection' and minor['type'] == 'FeatureCollection':
        arc = dist/6371000*180/math.pi*2
        for minorfeature in minor['features']:
            minorgeom = minorfeature['geometry']
            minorlng = minorgeom['coordinates'][0]
            minorlat = minorgeom['coordinates'][1]

            is_accept = True
            for mainfeature in major['features']:
                maingeom = mainfeature['geometry']
                mainlng = maingeom['coordinates'][0]
                mainlat = maingeom['coordinates'][1]
          
                if abs(minorlat-mainlat) <= arc and abs(minorlng-mainlng) <= arc:
                    distance = point_distance(maingeom, minorgeom)
                    if distance < dist:
                        is_accept = False
                        break
            if is_accept:
                result["features"].append(minorfeature)
    return result

def get_endpoint_from_points(points):
    """

    """
    count = 0 
    result = deepcopy(points)
    if points['type'] == 'FeatureCollection':
        feature_count = len(points['features'])
        for i in range(0, feature_count):
            first_geom = points['features'][i]['geometry']
            first_lng = first_geom['coordinates'][0]
            first_lat = first_geom['coordinates'][1]

            for j in range(0, feature_count):
                if i == j:
                    continue
                second_geom = points['features'][j]['geometry']
                second_lng = second_geom['coordinates'][0]
                second_lat = second_geom['coordinates'][1]

                if first_lat == second_lat and first_lng == second_lng:
                    result['features'].remove(points['features'][i])
                    count += 1
                    break
    return result


def get_endpoint_from_linestring(linestrings):
    """
    """
    points = get_bothend_from_linestring(linestrings)
    return get_endpoint_from_points(points)

def get_bothend_from_linestring(linestrings):
    """

    """
    points = []

    for linestring in linestrings['features']:
        coord = linestring['geometry']['coordinates']
        properties = linestring['properties']
        first = coord[0]
        first_feat = get_point_feature(first, properties)
        last = coord[len(coord)-1]
        last_feat = get_point_feature(last, properties)
        points.append(first_feat)
        points.append(last_feat)
    return FeatureCollection(points)

def get_point_feature(coord, properties):
    return Feature(geometry=Point(coord), properties=properties)


