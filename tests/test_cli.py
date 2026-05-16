import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from geojson_utils.cli import main


class CliTest(unittest.TestCase):
    def _write_geojson(self, tmpdir, name, value):
        path = os.path.join(tmpdir, name)
        with open(path, "w", encoding="utf-8") as fp:
            json.dump(value, fp)
        return path

    def test_validate_command(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write_geojson(tmpdir, "point.geojson", {"type": "Point", "coordinates": [1, 2]})
            output = io.StringIO()

            with redirect_stdout(output):
                code = main(["validate", path])

        self.assertEqual(code, 0)
        self.assertEqual(output.getvalue(), "valid\n")

    def test_convert_command_writes_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write_geojson(tmpdir, "point.geojson", {"type": "Point", "coordinates": [1, 2]})
            output = io.StringIO()

            with redirect_stdout(output):
                code = main(["convert", path, "--to", "json"])

        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue()), {"type": "Point", "coordinates": [1, 2]})

    def test_bbox_command(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write_geojson(tmpdir, "line.geojson", {"type": "LineString", "coordinates": [[2, 3], [1, 4]]})
            output = io.StringIO()

            with redirect_stdout(output):
                code = main(["bbox", path])

        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue()), [1, 3, 2, 4])

    def test_simplify_command(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = self._write_geojson(
                tmpdir,
                "line.geojson",
                {"type": "LineString", "coordinates": [[0, 0], [0.001, 0.00001], [0.002, 0]]},
            )
            output = io.StringIO()

            with redirect_stdout(output):
                code = main(["simplify", path, "--tolerance", "20"])

        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue()), {"type": "LineString", "coordinates": [[0, 0], [0.002, 0]]})


if __name__ == "__main__":
    unittest.main()
