"""
Moving Average demand forecaster.
Baseline implementation using a simple N-day moving average.
Extension path: replace with ARIMA, Prophet, or LSTM via BaseForecaster.
"""
from datetime import date, timedelta
from typing import List

from ai.interfaces.base_forecaster import BaseForecaster
from ai.schemas.ai_schemas import ForecastInput, ForecastOutput, ForecastPoint


class MovingAverageForecaster(BaseForecaster):
    """Simple Moving Average forecaster (v1 baseline)."""

    def predict(self, input_data: ForecastInput) -> ForecastOutput:
        """
        Forecast using a rolling average of the last `window_size` historical points.
        If fewer data points than window_size exist, uses all available points.
        If no historical data available, returns zero forecasts.
        """
        historical = input_data.historical_data
        window = min(input_data.window_size, len(historical)) if historical else 0

        if window == 0:
            average_demand = 0.0
            explanation = (
                "No historical data available. Forecast defaults to zero demand."
            )
        else:
            recent_data = historical[-window:]
            average_demand = sum(p.quantity for p in recent_data) / window
            explanation = (
                f"Moving average over the last {window} data point(s): "
                f"average daily demand = {average_demand:.2f} units. "
                f"Forecast applies this average for the next {input_data.horizon_days} days."
            )

        daily_forecasts = self._generate_daily_forecasts(
            average_demand, input_data.horizon_days
        )
        total_demand = sum(p.predicted_quantity for p in daily_forecasts)

        return ForecastOutput(
            product_id=input_data.product_id,
            method="moving_average",
            horizon_days=input_data.horizon_days,
            daily_forecasts=daily_forecasts,
            total_predicted_demand=round(total_demand, 2),
            explanation=explanation,
        )

    @staticmethod
    def _generate_daily_forecasts(
        daily_demand: float, horizon_days: int
    ) -> List[ForecastPoint]:
        today = date.today()
        return [
            ForecastPoint(
                date=(today + timedelta(days=i)).isoformat(),
                predicted_quantity=round(daily_demand, 4),
                confidence=0.70 if daily_demand > 0 else None,
            )
            for i in range(1, horizon_days + 1)
        ]
