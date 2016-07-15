

def join_featurecollection(*jsons):
    features = []
    for json in jsons:
        if json['type'] == 'FeatureCollection':
            for feature in json['features']:
                features.append(feature)
    return {"type":'FeatureCollection',"features":features}


def main():
    first_str = """
    { "type": "FeatureCollection",
    "features": [
      { "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
        "properties": {"prop0": "value0"}
        },
      { "type": "Feature",
        "geometry": {
          "type": "LineString",
          "coordinates": [
            [102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]
            ]
          },
        "properties": {
          "prop0": "value0",
          "prop1": 0.0
          }
        },
      { "type": "Feature",
         "geometry": {
           "type": "Polygon",
           "coordinates": [
             [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
               [100.0, 1.0], [100.0, 0.0] ]
             ]
         },
         "properties": {
           "prop0": "value0",
           "prop1": {"this": "that"}
           }
         }
       ]
     }
    """
    first = json.loads(first_str)
    second_str = """
     { "type": "FeatureCollection",
    "features": [
      { "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
        "properties": {"prop0": "value0"}
        },
      { "type": "Feature",
        "geometry": {
          "type": "point",
          "coordinates": [20, 0.0]
          },
        "properties": {
          "prop0": "value0",
          "prop1": 0.0
          }
        }
       ]
     }
    """
    second = json.loads(second_str)
    print(join_featurecollection(first, second))

if __name__ == '__main__':
    main()

