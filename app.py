
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.sensor_simulator import generate_sensor_readings
from src.water_analysis import (
    calculate_water_statistics,
    calculate_hourly_consumption,
    calculate_daily_consumption
)
from src.leak_detection import detect_water_leaks


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AquaGuard | Smart Water Intelligence",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM DESIGN
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #08131d;
    color: #e8f0f7;
}

[data-testid="stHeader"] {
    background: #08131d;
}

[data-testid="stSidebar"] {
    background: #101e2a;
    border-right: 1px solid #263746;
}

[data-testid="stSidebar"] * {
    color: #e8f0f7;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

h1, h2, h3, p, label {
    color: #e8f0f7;
}

.dashboard-title {
    font-size: 30px;
    font-weight: 750;
    color: #f1f6fb;
    margin-bottom: 4px;
}

.dashboard-subtitle {
    color: #91a7b8;
    font-size: 14px;
    margin-bottom: 24px;
}

.section-title {
    font-size: 18px;
    font-weight: 650;
    color: #e8f0f7;
    margin-bottom: 12px;
}

.metric-card {
    background: linear-gradient(145deg, #142635, #10202c);
    border: 1px solid #263b4c;
    border-radius: 13px;
    padding: 19px 17px;
    min-height: 140px;
}

.metric-label {
    color: #a6b8c7;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    margin-bottom: 13px;
}

.metric-value {
    color: #f4f8fc;
    font-size: 27px;
    font-weight: 750;
    margin-bottom: 6px;
}

.metric-description {
    color: #91a8b9;
    font-size: 12px;
}

.metric-blue {
    color: #36a2ff;
}

.metric-green {
    color: #12c98b;
}

.metric-red {
    color: #ff626b;
}

.panel {
    background: #101f2b;
    border: 1px solid #263b4b;
    border-radius: 13px;
    padding: 18px;
}

.panel-heading {
    color: #eaf2f8;
    font-size: 17px;
    font-weight: 650;
    margin-bottom: 5px;
}

.panel-subtitle {
    color: #8299aa;
    font-size: 12px;
    margin-bottom: 15px;
}

.status-row {
    display: flex;
    justify-content: space-between;
    padding: 12px 0;
    border-bottom: 1px solid #263b4b;
    color: #dce8f0;
    font-size: 13px;
}

.alert-card {
    background: #182b38;
    border-left: 4px solid #ff626b;
    border-radius: 8px;
    padding: 13px;
    margin-bottom: 12px;
}

.alert-title {
    color: #ff7279;
    font-size: 14px;
    font-weight: 650;
}

.alert-description {
    color: #a9bbc9;
    font-size: 12px;
    margin-top: 5px;
}

.success-card {
    background: #102d2a;
    border: 1px solid #17664f;
    border-radius: 9px;
    padding: 15px;
    color: #39d5a0;
}

.stButton button,
.stDownloadButton button {
    background: #137bd1;
    color: white;
    border: none;
    border-radius: 7px;
    font-weight: 600;
}

.stButton button:hover,
.stDownloadButton button:hover {
    background: #2196ed;
    color: white;
}

[data-testid="stMetric"] {
    background: #142635;
    border: 1px solid #263b4c;
    border-radius: 10px;
    padding: 15px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #263b4c;
    border-radius: 8px;
}

hr {
    border-color: #263b4b;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATA
# =========================================================

@st.cache_data(ttl=60)
def load_sensor_data():
    return generate_sensor_readings(
        num_readings=43200,
        seed=42
    )


data = load_sensor_data()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def metric_card(title, value, description, color="metric-blue"):

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{title}</div>
            <div class="metric-value {color}">{value}</div>
            <div class="metric-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def dark_chart(fig, height=320):

    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="#a9bdcc",
            family="Arial"
        ),
        margin=dict(
            l=10,
            r=10,
            t=35,
            b=10
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            gridcolor="#263b4b",
            zeroline=False
        )
    )

    return fig


def page_header(title, subtitle):

    st.markdown(
        f"""
        <div class="dashboard-title">{title}</div>
        <div class="dashboard-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True
    )


def make_csv_download(df, filename, label):

    st.download_button(
        label=label,
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=filename,
        mime="text/csv",
        use_container_width=False
    )


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.markdown(
    """
    <h1 style="color:#36a2ff;font-size:29px;">
        💧 AquaGuard
    </h1>
    <p style="color:#91a7b8;font-size:11px;">
        SMART WATER INTELLIGENCE
    </p>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "MAIN MENU",
    [
        "Dashboard",
        "Sensor Readings",
        "Leakage Alerts",
        "Water Analytics"
    ],
    key="main_navigation"
)

st.sidebar.markdown("---")

st.sidebar.markdown("### Monitoring Settings")

flow_threshold = st.sidebar.slider(
    "Leak Detection Threshold (L/min)",
    min_value=5,
    max_value=20,
    value=10
)

consecutive_readings = st.sidebar.slider(
    "Continuous Readings Required",
    min_value=2,
    max_value=15,
    value=5
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <div style="
        background:#172b3a;
        padding:14px;
        border-radius:10px;
    ">
        <div style="color:#12c98b;font-weight:650;">
            ● SENSOR SIMULATION ACTIVE
        </div>
        <div style="color:#91a7b8;font-size:12px;margin-top:8px;">
            Monitoring mode: Demonstration
        </div>
        <div style="color:#91a7b8;font-size:12px;">
            Connected sensors: 1 simulated sensor
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "AquaGuard Water Monitoring System"
)


# =========================================================
# ANALYSIS
# =========================================================

statistics = calculate_water_statistics(data)

hourly_data = calculate_hourly_consumption(data)

daily_data = calculate_daily_consumption(data)

leak_alerts = detect_water_leaks(
    data,
    flow_threshold,
    consecutive_readings
)

latest_flow = float(data["flow_rate_lpm"].iloc[-1])

today = pd.Timestamp.now().date()

today_data = data[
    pd.to_datetime(data["timestamp"]).dt.date == today
]

today_consumption = today_data[
    "consumption_liters"
].sum()

total_consumption = statistics["total_consumption"]

alarm_count = len(leak_alerts)


# =========================================================
# PAGE 1: DASHBOARD
# =========================================================

if page == "Dashboard":

    page_header(
        "💧 AquaGuard Water Intelligence",
        "Smart water consumption monitoring and leakage detection"
    )

    # Top metric cards
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        metric_card(
            "CURRENT FLOW",
            f"{latest_flow:.2f} L/min",
            "Latest sensor reading",
            "metric-blue"
        )

    with c2:
        metric_card(
            "WATER TODAY",
            f"{today_consumption:.2f} L",
            "Today's consumption",
            "metric-green"
        )

    with c3:
        metric_card(
            "TOTAL CONSUMPTION",
            f"{total_consumption:.1f} L",
            "Last 30 days",
            "metric-blue"
        )

    with c4:
        metric_card(
            "SENSOR STATUS",
            "ONLINE",
            "1 simulated sensor",
            "metric-green"
        )

    with c5:
        metric_card(
            "LEAKAGE ALERTS",
            str(alarm_count),
            "Potential events detected",
            "metric-red" if alarm_count else "metric-green"
        )

    st.write("")

    # Main chart and sensor status
    left, right = st.columns([1.6, 1])

    with left:

        st.markdown(
            '<div class="panel-heading">Water Consumption - Last 30 Days</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="panel-subtitle">Daily water usage trend</div>',
            unsafe_allow_html=True
        )

        trend = px.line(
            daily_data,
            x="date",
            y="water_consumption",
            markers=True
        )

        trend.update_traces(
            line=dict(color="#2699f5", width=3),
            marker=dict(size=6),
            fill="tozeroy",
            fillcolor="rgba(38,153,245,0.12)"
        )

        trend.update_layout(
            xaxis_title="Date",
            yaxis_title="Water Consumption (Liters)"
        )

        st.plotly_chart(
            dark_chart(trend, 350),
            use_container_width=True
        )

    with right:

        st.markdown(
            '<div class="panel-heading">Sensor Communication Status</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="panel-subtitle">Current sensor availability</div>',
            unsafe_allow_html=True
        )

        sensor_status = go.Figure(
            go.Pie(
                labels=["Online"],
                values=[1],
                hole=0.72,
                marker=dict(colors=["#12c98b"]),
                textinfo="none"
            )
        )

        sensor_status.update_layout(
            annotations=[
                dict(
                    text="1",
                    x=0.5,
                    y=0.5,
                    font=dict(size=35, color="white"),
                    showarrow=False
                )
            ],
            showlegend=False
        )

        st.plotly_chart(
            dark_chart(sensor_status, 235),
            use_container_width=True
        )

        st.markdown(
            """
            <div class="status-row">
                <span>🟢 Online</span>
                <b>1 (100%)</b>
            </div>
            <div class="status-row">
                <span>⚪ Offline</span>
                <b>0 (0%)</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # Bottom panels
    b1, b2, b3 = st.columns([1.2, 1, 1.2])

    with b1:

        st.markdown(
            '<div class="panel-heading">Hourly Water Consumption</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="panel-subtitle">Usage distribution by hour</div>',
            unsafe_allow_html=True
        )

        hourly_chart = px.bar(
            hourly_data.tail(24),
            x="hour",
            y="water_consumption"
        )

        hourly_chart.update_traces(
            marker_color="#258ee0"
        )

        hourly_chart.update_layout(
            xaxis_title="Hour",
            yaxis_title="Liters"
        )

        st.plotly_chart(
            dark_chart(hourly_chart, 280),
            use_container_width=True
        )

    with b2:

        st.markdown(
            '<div class="panel-heading">Water Flow Statistics</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="panel-subtitle">Sensor performance summary</div>',
            unsafe_allow_html=True
        )

        stats_rows = [
            ("Average Flow", f"{statistics['average_flow']:.2f} L/min"),
            ("Maximum Flow", f"{statistics['maximum_flow']:.2f} L/min"),
            ("Total Readings", f"{statistics['total_readings']:,}"),
            ("Today's Usage", f"{today_consumption:.2f} L"),
            ("Sensor Status", "Active")
        ]

        for label, value in stats_rows:
            st.markdown(
                f"""
                <div class="status-row">
                    <span>{label}</span>
                    <b>{value}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

    with b3:

        st.markdown(
            '<div class="panel-heading">Latest Leakage Alerts</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="panel-subtitle">Potential abnormal water-flow events</div>',
            unsafe_allow_html=True
        )

        if leak_alerts.empty:

            st.markdown(
                """
                <div class="success-card">
                    ✓ No potential leakage detected.
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            for _, alert in leak_alerts.tail(3).iloc[::-1].iterrows():

                st.markdown(
                    f"""
                    <div class="alert-card">
                        <div class="alert-title">
                            ⚠ Potential Water Leakage
                        </div>
                        <div class="alert-description">
                            Start: {alert['start_time']}<br>
                            Duration: {alert['duration_minutes']} minutes<br>
                            Average flow: {alert['average_flow_lpm']} L/min
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown("---")

    st.caption(
        "AquaGuard | Smart Water Consumption Monitoring "
        "| Simulated IoT Sensor Data"
    )


# =========================================================
# PAGE 2: SENSOR READINGS
# =========================================================

elif page == "Sensor Readings":

    page_header(
        "📡 Sensor Readings",
        "Detailed water-flow monitoring and sensor data analysis"
    )

    sensor_dates = pd.to_datetime(data["timestamp"]).dt.date

    min_date = sensor_dates.min()
    max_date = sensor_dates.max()

    st.markdown("### Reading Filters")

    f1, f2 = st.columns(2)

    with f1:

        selected_dates = st.date_input(
            "Select date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

    with f2:

        max_flow = max(
            1.0,
            float(data["flow_rate_lpm"].max())
        )

        flow_range = st.slider(
            "Flow Rate Range (L/min)",
            min_value=0.0,
            max_value=float(max_flow + 1),
            value=(0.0, float(max_flow + 1))
        )

    filtered_data = data.copy()

    if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:

        start_date, end_date = selected_dates

        filtered_data = filtered_data[
            (sensor_dates >= start_date) &
            (sensor_dates <= end_date)
        ]

    filtered_data = filtered_data[
        (filtered_data["flow_rate_lpm"] >= flow_range[0]) &
        (filtered_data["flow_rate_lpm"] <= flow_range[1])
    ]

    st.markdown("---")

    st.markdown("### Sensor Reading Overview")

    if filtered_data.empty:

        st.warning("No readings match the selected filters.")

    else:

        filtered_stats = calculate_water_statistics(
            filtered_data
        )

        m1, m2, m3, m4 = st.columns(4)

        with m1:
            metric_card(
                "TOTAL READINGS",
                f"{filtered_stats['total_readings']:,}",
                "Filtered readings"
            )

        with m2:
            metric_card(
                "AVERAGE FLOW",
                f"{filtered_stats['average_flow']:.2f}",
                "Liters per minute",
                "metric-green"
            )

        with m3:
            metric_card(
                "MAXIMUM FLOW",
                f"{filtered_stats['maximum_flow']:.2f}",
                "Liters per minute",
                "metric-blue"
            )

        with m4:
            metric_card(
                "WATER CONSUMPTION",
                f"{filtered_stats['total_consumption']:.2f} L",
                "Selected period",
                "metric-green"
            )

        st.write("")

        st.markdown("### Water Flow Rate Analysis")

        flow_chart = px.line(
            filtered_data.tail(1000),
            x="timestamp",
            y="flow_rate_lpm"
        )

        flow_chart.update_traces(
            line=dict(color="#2699f5", width=2)
        )

        flow_chart.add_hline(
            y=flow_threshold,
            line_dash="dash",
            line_color="#ff626b",
            annotation_text="Leakage Threshold"
        )

        flow_chart.update_layout(
            xaxis_title="Time",
            yaxis_title="Flow Rate (L/min)"
        )

        st.plotly_chart(
            dark_chart(flow_chart, 340),
            use_container_width=True
        )

        st.markdown("### Water Consumption Analysis")

        consumption_chart = px.area(
            filtered_data.tail(1000),
            x="timestamp",
            y="consumption_liters"
        )

        consumption_chart.update_traces(
            line_color="#12c98b",
            fillcolor="rgba(18,201,139,0.15)"
        )

        consumption_chart.update_layout(
            xaxis_title="Time",
            yaxis_title="Consumption (Liters)"
        )

        st.plotly_chart(
            dark_chart(consumption_chart, 300),
            use_container_width=True
        )

        st.markdown("### Detailed Sensor Records")

        display_data = filtered_data.sort_values(
            "timestamp",
            ascending=False
        ).copy()

        display_data["Reading Status"] = display_data[
            "flow_rate_lpm"
        ].apply(
            lambda value: (
                "Potential High Flow"
                if value > flow_threshold
                else "Normal"
            )
        )

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )

        make_csv_download(
            display_data,
            "aquaguard_sensor_readings.csv",
            "⬇ Download Filtered Sensor Data"
        )

    st.markdown("---")

    st.caption("AquaGuard | Sensor Readings")


# =========================================================
# PAGE 3: LEAKAGE ALERTS
# =========================================================

elif page == "Leakage Alerts":

    page_header(
        "🚨 Leakage Detection Center",
        "Identify and review unusual water-flow events"
    )

    a1, a2, a3 = st.columns(3)

    with a1:
        metric_card(
            "TOTAL ALERTS",
            str(alarm_count),
            "Detected potential events",
            "metric-red" if alarm_count else "metric-green"
        )

    with a2:
        metric_card(
            "FLOW THRESHOLD",
            f"{flow_threshold} L/min",
            "Current detection setting"
        )

    with a3:
        metric_card(
            "MINIMUM DURATION",
            f"{consecutive_readings} min",
            "Continuous high flow required"
        )

    st.write("")

    st.markdown("### Alert Status")

    if leak_alerts.empty:

        st.markdown(
            """
            <div class="success-card">
                ✓ No potential water leakage detected
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.error(
            f"{alarm_count} potential water leakage event(s) detected."
        )

        for index, alert in leak_alerts.iterrows():

            with st.expander(
                f"⚠ Alert {index + 1} - {alert['alert']}"
            ):

                col1, col2 = st.columns(2)

                col1.metric(
                    "Duration",
                    f"{alert['duration_minutes']} minutes"
                )

                col2.metric(
                    "Average Flow",
                    f"{alert['average_flow_lpm']} L/min"
                )

                st.write(
                    "**Start time:**",
                    alert["start_time"]
                )

                st.write(
                    "**End time:**",
                    alert["end_time"]
                )

                st.write(
                    "**Maximum flow:**",
                    f"{alert['maximum_flow_lpm']} L/min"
                )

                st.warning(
                    "This is a simulated potential leakage alert. "
                    "Inspect the water system before confirming an actual leak."
                )

        st.markdown("### Complete Alert Records")

        st.dataframe(
            leak_alerts,
            use_container_width=True,
            hide_index=True
        )

        make_csv_download(
            leak_alerts,
            "aquaguard_leakage_alerts.csv",
            "⬇ Download Leakage Alert Report"
        )

    st.markdown("---")

    st.markdown("### Water Flow During Detected Events")

    if not leak_alerts.empty:

        flagged = data[
            data["flow_rate_lpm"] > flow_threshold
        ].copy()

        if not flagged.empty:

            alert_chart = px.scatter(
                flagged,
                x="timestamp",
                y="flow_rate_lpm",
                title="Readings Above Leakage Threshold"
            )

            alert_chart.update_traces(
                marker=dict(
                    color="#ff626b",
                    size=7
                )
            )

            alert_chart.add_hline(
                y=flow_threshold,
                line_dash="dash",
                line_color="#f5bb42"
            )

            st.plotly_chart(
                dark_chart(alert_chart, 320),
                use_container_width=True
            )

    else:

        st.info(
            "The alert chart will appear when potential high-flow "
            "events are detected."
        )

    st.caption("AquaGuard | Leakage Detection Center")


# =========================================================
# PAGE 4: WATER ANALYTICS
# =========================================================

elif page == "Water Analytics":

    page_header(
        "📊 Water Analytics",
        "Understand water consumption patterns and trends"
    )

    st.markdown("### Consumption Overview")

    m1, m2, m3 = st.columns(3)

    with m1:
        metric_card(
            "TOTAL CONSUMPTION",
            f"{total_consumption:.2f} L",
            "Last 30 days"
        )

    with m2:
        metric_card(
            "AVERAGE DAILY USAGE",
            f"{daily_data['water_consumption'].mean():.2f} L",
            "Average per day",
            "metric-green"
        )

    with m3:
        metric_card(
            "HIGHEST DAILY USAGE",
            f"{daily_data['water_consumption'].max():.2f} L",
            "Maximum daily consumption",
            "metric-blue"
        )

    st.write("")

    st.markdown("### Daily Water Consumption")

    daily_chart = px.bar(
        daily_data,
        x="date",
        y="water_consumption"
    )

    daily_chart.update_traces(
        marker_color="#258ee0"
    )

    daily_chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Consumption (Liters)"
    )

    st.plotly_chart(
        dark_chart(daily_chart, 350),
        use_container_width=True
    )

    st.markdown("### Hourly Water Consumption")

    hourly_chart = px.line(
        hourly_data.tail(24),
        x="hour",
        y="water_consumption",
        markers=True
    )

    hourly_chart.update_traces(
        line=dict(color="#12c98b", width=3),
        marker=dict(size=7)
    )

    hourly_chart.update_layout(
        xaxis_title="Hour",
        yaxis_title="Consumption (Liters)"
    )

    st.plotly_chart(
        dark_chart(hourly_chart, 330),
        use_container_width=True
    )

    st.markdown("### Consumption Data Tables")

    tab1, tab2 = st.tabs([
        "Daily Records",
        "Hourly Records"
    ])

    with tab1:

        st.dataframe(
            daily_data,
            use_container_width=True,
            hide_index=True
        )

        make_csv_download(
            daily_data,
            "aquaguard_daily_analytics.csv",
            "⬇ Download Daily Analytics"
        )

    with tab2:

        st.dataframe(
            hourly_data,
            use_container_width=True,
            hide_index=True
        )

        make_csv_download(
            hourly_data,
            "aquaguard_hourly_analytics.csv",
            "⬇ Download Hourly Analytics"
        )

    st.markdown("---")

    st.caption("AquaGuard | Water Consumption Analytics")


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#8198a9;
        font-size:12px;
        padding:10px;
    ">
        💧 AquaGuard Smart Water Monitoring System
        <br>
        Built using Python, Streamlit, Pandas and Plotly
        <br>
        Demonstration using simulated IoT sensor data
    </div>
    """,
    unsafe_allow_html=True
)
