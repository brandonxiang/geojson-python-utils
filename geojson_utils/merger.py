import math
from copy import deepcopy
from geojson_utils import point_distance

def merge_featurecollection(*jsons):
    features = []
    for json in jsons:
        if json['type'] == 'FeatureCollection':
            for feature in json['features']:
                features.append(feature)
    return {"type":'FeatureCollection', "features":features}

def simplify_other(major, minor, dist):
    """
    point featurecollection only
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