
import pandas as pd


def detect_water_leaks(
    data,
    flow_threshold=10,
    consecutive_readings=5
):
    """
    Detect continuous unusually high water flow.

    Each reading represents one minute.
    A potential leak is flagged when flow exceeds
    the threshold for the required consecutive readings.
    """

    columns = [
        "start_time",
        "end_time",
        "duration_minutes",
        "average_flow_lpm",
        "maximum_flow_lpm",
        "alert"
    ]

    if data.empty:
        return pd.DataFrame(columns=columns)

    results = data.copy().reset_index(drop=True)

    high_flow = (
        results["flow_rate_lpm"] > flow_threshold
    )

    # Assign a group number whenever the flow condition changes.
    groups = high_flow.ne(high_flow.shift()).cumsum()

    alerts = []

    for _, group in results.groupby(groups):

        if (
            bool(group["flow_rate_lpm"].gt(flow_threshold).all())
            and len(group) >= consecutive_readings
        ):

            alerts.append({
                "start_time": group["timestamp"].iloc[0],
                "end_time": group["timestamp"].iloc[-1],
                "duration_minutes": len(group),
                "average_flow_lpm": round(
                    group["flow_rate_lpm"].mean(), 2
                ),
                "maximum_flow_lpm": round(
                    group["flow_rate_lpm"].max(), 2
                ),
                "alert": "Potential Water Leakage"
            })

    return pd.DataFrame(alerts, columns=columns)


if __name__ == "__main__":
    from sensor_simulator import generate_sensor_readings

    readings = generate_sensor_readings()

    alerts = detect_water_leaks(readings)

    if alerts.empty:
        print("No potential leakage detected.")
    else:
        print("POTENTIAL WATER LEAKAGE")
        print(alerts.to_string(index=False))
