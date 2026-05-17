from typing import Any, MutableMapping, Optional

GeoJSON = MutableMapping[str, Any]


class OptionalAdapterError(ImportError):
    """Raised when an optional geospatial file adapter dependency is missing."""


def _load_geopandas():
    try:
        import geopandas
    except ImportError as exc:
        raise OptionalAdapterError(
            "Shapefile and GeoPackage adapters require optional dependency 'geopandas'. "
            "Install it with geojson_utils[files] once the extra is available."
        ) from exc
    return geopandas


def read_vector_file(path: str, *, driver: Optional[str] = None) -> GeoJSON:
    """Read a Shapefile/GeoPackage-style vector file as a GeoJSON FeatureCollection."""
    geopandas = _load_geopandas()
    frame = geopandas.read_file(path, driver=driver)
    return frame.__geo_interface__


def write_vector_file(value: GeoJSON, path: str, *, driver: Optional[str] = None) -> None:
    """Write a GeoJSON FeatureCollection to a Shapefile/GeoPackage-style vector file."""
    geopandas = _load_geopandas()
    frame = geopandas.GeoDataFrame.from_features(value.get("features", []))
    frame.to_file(path, driver=driver)


def read_shapefile(path: str) -> GeoJSON:
    """Read a Shapefile into a GeoJSON FeatureCollection."""
    return read_vector_file(path)


def write_shapefile(value: GeoJSON, path: str) -> None:
    """Write a GeoJSON FeatureCollection to a Shapefile."""
    write_vector_file(value, path, driver="ESRI Shapefile")


def read_geopackage(path: str, *, layer: Optional[str] = None) -> GeoJSON:
    """Read a GeoPackage layer into a GeoJSON FeatureCollection."""
    geopandas = _load_geopandas()
    frame = geopandas.read_file(path, layer=layer)
    return frame.__geo_interface__


def write_geopackage(value: GeoJSON, path: str, *, layer: str = "features") -> None:
    """Write a GeoJSON FeatureCollection to a GeoPackage layer."""
    geopandas = _load_geopandas()
    frame = geopandas.GeoDataFrame.from_features(value.get("features", []))
    frame.to_file(path, layer=layer, driver="GPKG")
