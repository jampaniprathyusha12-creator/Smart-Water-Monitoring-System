
import pandas as pd


def calculate_water_statistics(data):
    """Calculate overall water consumption statistics."""

    if data.empty:
        return {
            "total_consumption": 0,
            "average_flow": 0,
            "maximum_flow": 0,
            "total_readings": 0
        }

    return {
        "total_consumption": round(
            data["consumption_liters"].sum(), 2
        ),
        "average_flow": round(
            data["flow_rate_lpm"].mean(), 2
        ),
        "maximum_flow": round(
            data["flow_rate_lpm"].max(), 2
        ),
        "total_readings": len(data)
    }


def calculate_hourly_consumption(data):
    """Calculate consumption grouped by hour."""

    if data.empty:
        return pd.DataFrame(
            columns=["hour", "water_consumption"]
        )

    hourly_data = data.copy()

    hourly_data["hour"] = (
        pd.to_datetime(hourly_data["timestamp"]).dt.floor("h")
    )

    result = (
        hourly_data.groupby("hour")["consumption_liters"]
        .sum()
        .reset_index()
    )

    result.columns = ["hour", "water_consumption"]

    return result


def calculate_daily_consumption(data):
    """Calculate consumption grouped by day."""

    if data.empty:
        return pd.DataFrame(
            columns=["date", "water_consumption"]
        )

    daily_data = data.copy()

    daily_data["date"] = (
        pd.to_datetime(daily_data["timestamp"]).dt.date
    )

    result = (
        daily_data.groupby("date")["consumption_liters"]
        .sum()
        .reset_index()
    )

    result.columns = ["date", "water_consumption"]

    return result
