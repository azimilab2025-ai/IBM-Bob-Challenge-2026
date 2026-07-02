"""
Basic Route Optimizer — Nearest Neighbor Heuristic.
Greedily visits the closest unvisited delivery stop at each step.
Extension path: 2-opt improvement → Christofides → full VRP.
"""
import math
from typing import List, Optional, Tuple

from ai.interfaces.base_route_optimizer import BaseRouteOptimizer
from ai.schemas.ai_schemas import DeliveryStop, RouteInput, RouteOutput, RouteStop


class NearestNeighborRouter(BaseRouteOptimizer):
    """Nearest-neighbor route optimizer (v1 baseline)."""

    def optimize(self, route_input: RouteInput) -> RouteOutput:
        if not route_input.stops:
            return RouteOutput(
                warehouse_id=route_input.warehouse_id,
                stops=[],
                total_distance_km=0.0,
                estimated_duration_minutes=0,
                explanation="No delivery stops provided.",
            )

        ordered_stops, total_distance = self._build_route(route_input)

        duration = (
            int(total_distance / 50 * 60 + len(ordered_stops) * 10)
            if total_distance is not None
            else None
        )

        explanation = (
            f"Nearest-neighbor heuristic applied to {len(ordered_stops)} delivery stop(s). "
            + (
                f"Estimated total route: {total_distance:.1f} km, ~{duration} minutes."
                if total_distance is not None
                else "Coordinates unavailable for some stops; distance estimation skipped."
            )
        )

        return RouteOutput(
            warehouse_id=route_input.warehouse_id,
            stops=ordered_stops,
            total_distance_km=round(total_distance, 2) if total_distance is not None else None,
            estimated_duration_minutes=duration,
            explanation=explanation,
        )

    def _build_route(
        self, route_input: RouteInput
    ) -> Tuple[List[RouteStop], Optional[float]]:
        unvisited = list(route_input.stops)
        ordered: List[RouteStop] = []
        total_distance = 0.0
        all_have_coords = True
        current_lat = route_input.warehouse_latitude
        current_lon = route_input.warehouse_longitude

        while unvisited:
            nearest, dist = self._find_nearest(current_lat, current_lon, unvisited)
            if dist is None:
                all_have_coords = False
            else:
                total_distance += dist

            ordered.append(RouteStop(
                sequence=len(ordered) + 1,
                order_id=nearest.order_id,
                delivery_address=nearest.delivery_address,
                latitude=nearest.latitude,
                longitude=nearest.longitude,
            ))
            current_lat = nearest.latitude
            current_lon = nearest.longitude
            unvisited.remove(nearest)

        return ordered, total_distance if all_have_coords else None

    @staticmethod
    def _find_nearest(
        current_lat: Optional[float],
        current_lon: Optional[float],
        stops: List[DeliveryStop],
    ) -> Tuple[DeliveryStop, Optional[float]]:
        if current_lat is None or current_lon is None:
            return stops[0], None

        nearest, min_dist = stops[0], float("inf")
        for stop in stops:
            if stop.latitude is None or stop.longitude is None:
                continue
            d = _haversine_km(current_lat, current_lon, stop.latitude, stop.longitude)
            if d < min_dist:
                min_dist, nearest = d, stop

        return nearest, min_dist if min_dist != float("inf") else None


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlambda = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
