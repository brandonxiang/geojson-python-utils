import argparse
import json
import sys
from typing import Any, Iterable, List, Optional, Sequence

from .converters import convert, read_geojson_auto
from .convertor import convertor
from .geojson_utils import simplify
from .validation import validate_geojson


def _read_input(path: str) -> Any:
    if path == "-":
        return json.loads(sys.stdin.read())
    return read_geojson_auto(path)


def _write_output(value: Any, path: Optional[str]) -> None:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)
    if path:
        with open(path, "w", encoding="utf-8") as fp:
            fp.write(text)
            fp.write("\n")
        return
    sys.stdout.write(text)
    sys.stdout.write("\n")


def _iter_coordinates(value: Any) -> Iterable[Sequence[float]]:
    if isinstance(value, dict):
        value_type = value.get("type")
        if value_type == "FeatureCollection":
            for feature in value.get("features", []):
                yield from _iter_coordinates(feature.get("geometry"))
        elif value_type == "Feature":
            yield from _iter_coordinates(value.get("geometry"))
        elif value_type == "GeometryCollection":
            for geometry in value.get("geometries", []):
                yield from _iter_coordinates(geometry)
        elif value_type == "Point":
            yield value["coordinates"]
        elif value_type in ("MultiPoint", "LineString"):
            for coordinate in value["coordinates"]:
                yield coordinate
        elif value_type in ("MultiLineString", "Polygon"):
            for line in value["coordinates"]:
                for coordinate in line:
                    yield coordinate
        elif value_type == "MultiPolygon":
            for polygon in value["coordinates"]:
                for ring in polygon:
                    for coordinate in ring:
                        yield coordinate


def _bbox(value: Any) -> List[float]:
    coords = list(_iter_coordinates(value))
    if not coords:
        raise ValueError("cannot calculate bbox for empty GeoJSON")
    xs = [coord[0] for coord in coords]
    ys = [coord[1] for coord in coords]
    return [min(xs), min(ys), max(xs), max(ys)]


def _cmd_validate(args: argparse.Namespace) -> int:
    validate_geojson(_read_input(args.input))
    print("valid")
    return 0


def _cmd_convert(args: argparse.Namespace) -> int:
    source = _read_input(args.input)
    result = convert(source, args.from_format, args.to_format)
    _write_output(result, args.output)
    return 0


def _cmd_transform(args: argparse.Namespace) -> int:
    source = _read_input(args.input)
    result = convertor(source, method=args.method)
    _write_output(result, args.output)
    return 0


def _cmd_simplify(args: argparse.Namespace) -> int:
    source = _read_input(args.input)
    if source.get("type") != "LineString":
        raise ValueError("simplify currently expects a LineString geometry")
    points = [{"type": "Point", "coordinates": coordinate} for coordinate in source["coordinates"]]
    result = {"type": "LineString", "coordinates": [point["coordinates"] for point in simplify(points, args.tolerance)]}
    _write_output(result, args.output)
    return 0


def _cmd_bbox(args: argparse.Namespace) -> int:
    _write_output(_bbox(_read_input(args.input)), args.output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="geojson-utils")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("input")
    validate_parser.set_defaults(func=_cmd_validate)

    convert_parser = subparsers.add_parser("convert")
    convert_parser.add_argument("input")
    convert_parser.add_argument("--from", dest="from_format", default="geojson")
    convert_parser.add_argument("--to", dest="to_format", required=True)
    convert_parser.add_argument("--output")
    convert_parser.set_defaults(func=_cmd_convert)

    transform_parser = subparsers.add_parser("transform")
    transform_parser.add_argument("input")
    transform_parser.add_argument("--method", default="wgs2gcj")
    transform_parser.add_argument("--output")
    transform_parser.set_defaults(func=_cmd_transform)

    simplify_parser = subparsers.add_parser("simplify")
    simplify_parser.add_argument("input")
    simplify_parser.add_argument("--tolerance", type=float, default=20)
    simplify_parser.add_argument("--output")
    simplify_parser.set_defaults(func=_cmd_simplify)

    bbox_parser = subparsers.add_parser("bbox")
    bbox_parser.add_argument("input")
    bbox_parser.add_argument("--output")
    bbox_parser.set_defaults(func=_cmd_bbox)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
