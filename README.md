# AquaGuard – Smart Water Monitoring System

## Project Overview

AquaGuard is a Smart Water Consumption Monitoring and Leak Alert System developed using Python and Streamlit.

The application monitors simulated water flow readings, calculates consumption, identifies unusual continuous water flow, and displays potential leakage alerts through an interactive dashboard.

## Features

- Water consumption monitoring
- Simulated IoT sensor readings
- Water flow analysis
- Potential leakage detection
- Daily and hourly consumption analytics
- Interactive dashboard
- Sensor data filtering
- CSV report downloads

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly

## Project Structure

```text
Smart-Water-Monitoring-System/
├── src/
├── data/
├── outputs/
├── screenshots/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project:

```bash
cd Smart-Water-Monitoring-System
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

## Working Principle

1. Generate simulated water flow sensor readings.
2. Process water consumption data.
3. Analyze hourly and daily usage.
4. Detect potential leakage based on continuous high flow.
5. Display results through the Streamlit dashboard.

## Project Type

Academic Practical Project – IoT and Environmental Technology.

## Note

This version uses simulated sensor readings for demonstration. Physical IoT hardware integration can be added as a future enhancement.