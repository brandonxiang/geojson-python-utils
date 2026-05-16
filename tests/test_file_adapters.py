import unittest

from geojson_utils import OptionalAdapterError, read_geopackage, read_shapefile, registered_converters


class FileAdapterTest(unittest.TestCase):
    def test_optional_adapter_error_is_clear(self):
        try:
            import geopandas  # noqa: F401
        except ImportError:
            with self.assertRaisesRegex(OptionalAdapterError, "geopandas"):
                read_shapefile("missing.shp")

    def test_file_converters_are_registered(self):
        self.assertIn(("shapefile", "geojson"), registered_converters())
        self.assertIn(("geopackage", "geojson"), registered_converters())

    def test_geopackage_missing_dependency_error_is_clear(self):
        try:
            import geopandas  # noqa: F401
        except ImportError:
            with self.assertRaisesRegex(OptionalAdapterError, "geopandas"):
                read_geopackage("missing.gpkg")


if __name__ == "__main__":
    unittest.main()
