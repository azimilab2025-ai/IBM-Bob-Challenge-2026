"""Abstract interface for warehouse allocation modules."""
from abc import ABC, abstractmethod

from ai.schemas.ai_schemas import AllocationOutput, AllocationRequest


class BaseAllocator(ABC):
    """
    All warehouse allocation implementations must implement this interface.
    """

    @abstractmethod
    def allocate(self, request: AllocationRequest) -> AllocationOutput:
        """
        Determine the best warehouse to fulfill an order.

        Args:
            request: Order items and available warehouse stock.

        Returns:
            AllocationOutput with the selected warehouse and explanation.
        """
        ...
