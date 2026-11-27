
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_sensor_readings(num_readings=43200, seed=42):
    """
    Generate 30 days of simulated water-flow readings.
    Each reading represents one minute.
    """

    rng = np.random.default_rng(seed)

    end_time = datetime.now().replace(second=0, microsecond=0)

    timestamps = pd.date_range(
        end=end_time,
        periods=num_readings,
        freq="min"
    )

    hours = timestamps.hour.to_numpy()

    # Normal usage is higher during morning and evening.
    peak_hours = (
        ((hours >= 6) & (hours <= 9)) |
        ((hours >= 18) & (hours <= 21))
    )

    base_flow = np.where(
        peak_hours,
        rng.uniform(3, 8, num_readings),
        rng.uniform(0, 2, num_readings)
    )

    flow_rates = np.maximum(
        0,
        base_flow + rng.normal(0, 0.3, num_readings)
    )

    # Simulate one unusual continuous water-flow event.
    if num_readings > 700:
        flow_rates[600:616] = rng.uniform(12, 16, 16)

    consumption = flow_rates / 60

    return pd.DataFrame({
        "timestamp": timestamps,
        "flow_rate_lpm": np.round(flow_rates, 2),
        "consumption_liters": np.round(consumption, 3)
    })


if __name__ == "__main__":
    readings = generate_sensor_readings()

    print("WATER SENSOR SIMULATION")
    print(readings.head(10).to_string(index=False))

    print("\nTotal consumption:")
    print(round(readings["consumption_liters"].sum(), 2), "liters")

    print("\nTotal readings:", len(readings))
