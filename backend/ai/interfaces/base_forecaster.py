"""Abstract interface for demand forecasting modules."""
from abc import ABC, abstractmethod

from ai.schemas.ai_schemas import ForecastInput, ForecastOutput


class BaseForecaster(ABC):
    """
    All demand forecasting implementations must implement this interface.
    Swap algorithms by providing a different implementation — no service changes required.
    """

    @abstractmethod
    def predict(self, input_data: ForecastInput) -> ForecastOutput:
        """
        Generate a demand forecast.

        Args:
            input_data: Historical data and forecast parameters.

        Returns:
            ForecastOutput with daily predictions and explanation.
        """
        ...
