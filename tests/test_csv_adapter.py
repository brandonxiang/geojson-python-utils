import csv
import io
import unittest

from geojson_utils import CSVGeoJSONError, convert, csv_to_feature_collection, feature_collection_to_csv


class CSVAdapterTest(unittest.TestCase):
    def test_csv_to_feature_collection(self):
        text = "id,longitude,latitude,name\n1,120.1,30.2,Hangzhou\n"

        result = csv_to_feature_collection(text, id_column="id")

        self.assertEqual(result["features"][0]["id"], "1")
        self.assertEqual(result["features"][0]["geometry"]["coordinates"], [120.1, 30.2])
        self.assertEqual(result["features"][0]["properties"], {"name": "Hangzhou"})

    def test_feature_collection_to_csv(self):
        collection = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "id": "1",
                    "geometry": {"type": "Point", "coordinates": [120.1, 30.2]},
                    "properties": {"name": "Hangzhou"},
                }
            ],
        }

        rows = list(csv.DictReader(io.StringIO(feature_collection_to_csv(collection, id_column="id"))))

        self.assertEqual(rows[0]["id"], "1")
        self.assertEqual(rows[0]["longitude"], "120.1")
        self.assertEqual(rows[0]["name"], "Hangzhou")

    def test_missing_coordinates_are_clear(self):
        with self.assertRaisesRegex(CSVGeoJSONError, "missing coordinate"):
            csv_to_feature_collection("name\nA\n")

    def test_registered_csv_converter(self):
        result = convert("longitude,latitude,name\n1,2,A\n", "csv", "geojson")

        self.assertEqual(result["features"][0]["properties"], {"name": "A"})
        self.assertIn("longitude,latitude,name", convert(result, "geojson", "csv"))


if __name__ == "__main__":
    unittest.main()
