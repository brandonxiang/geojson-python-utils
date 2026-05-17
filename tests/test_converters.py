import json
import os
import tempfile
import unittest

from geojson_utils import (
    GeoJSONConversionError,
    convert,
    read_geojson,
    registered_converters,
    write_geojson,
)


POINT = {"type": "Point", "coordinates": [1, 2]}


class ConverterTest(unittest.TestCase):
    def test_registered_json_converter_round_trip(self):
        text = convert(POINT, "geojson", "json")

        self.assertEqual(json.loads(text), POINT)
        self.assertEqual(convert(text, "json", "geojson"), POINT)

    def test_missing_converter_has_clear_error(self):
        with self.assertRaisesRegex(GeoJSONConversionError, "no converter registered"):
            convert(POINT, "geojson", "unknown")

    def test_geojson_file_io_validates_content(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "point.geojson")
            write_geojson(POINT, path)

            self.assertEqual(read_geojson(path), POINT)

    def test_registered_pairs_are_available(self):
        self.assertIn(("geojson", "json"), registered_converters())
        self.assertIn(("json", "geojson"), registered_converters())


if __name__ == "__main__":
    unittest.main()
