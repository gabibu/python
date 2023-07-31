from shapely.geometry import Polygon

from decision_maker.entities.vehicle_identifications import PolygonCoordinates


def _polygon_coordinates_to_polygon(polygon_coordinates: PolygonCoordinates) -> Polygon:
    return Polygon([(point.x, point.y) for point in polygon_coordinates.points])


def calculate_iou(polygon_coordinates1: PolygonCoordinates, polygon_coordinates2: PolygonCoordinates) -> float:
    poly_1 = _polygon_coordinates_to_polygon(polygon_coordinates1)
    poly_2 = _polygon_coordinates_to_polygon(polygon_coordinates2)
    return poly_1.intersection(poly_2).area / poly_1.union(poly_2).area
