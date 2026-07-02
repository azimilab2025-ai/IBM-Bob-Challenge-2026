"""Abstract interface for route optimization modules."""
from abc import ABC, abstractmethod

from ai.schemas.ai_schemas import RouteInput, RouteOutput


class BaseRouteOptimizer(ABC):
    """
    All route optimization implementations must implement this interface.
    """

    @abstractmethod
    def optimize(self, route_input: RouteInput) -> RouteOutput:
        """
        Compute an optimized delivery route.

        Args:
            route_input: Warehouse origin and list of delivery stops.

        Returns:
            RouteOutput with ordered stops and distance estimate.
        """
        ...
