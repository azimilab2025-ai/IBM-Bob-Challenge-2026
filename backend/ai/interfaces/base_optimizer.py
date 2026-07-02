"""Abstract interface for inventory optimization modules."""
from abc import ABC, abstractmethod

from ai.schemas.ai_schemas import InventoryOptimizationInput, InventoryOptimizationOutput


class BaseInventoryOptimizer(ABC):
    """
    All inventory optimization implementations must implement this interface.
    """

    @abstractmethod
    def optimize(self, input_data: InventoryOptimizationInput) -> InventoryOptimizationOutput:
        """
        Calculate optimal inventory parameters.

        Args:
            input_data: Demand statistics, cost parameters, and lead time.

        Returns:
            InventoryOptimizationOutput with safety stock, reorder point, and EOQ.
        """
        ...
