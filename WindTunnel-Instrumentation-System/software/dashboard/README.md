# Dashboard Usage Guide

## Wind Tunnel Data Acquisition and Visualization Dashboard

---

## Overview

This dashboard is used to visualize and record aerodynamic data collected from the wind tunnel instrumentation system.

It reads real-time sensor data from the Arduino via serial communication and displays:

* Lift force
* Drag force
* Airspeed
* Temperature
* Pressure
* Coefficient of Lift (CL)
* Coefficient of Drag (CD)

The dashboard also generates graphs and stores experimental data in CSV format.

---

## Software Requirements

Python 3.9 or later

Required Python packages:

* streamlit
* pandas
* matplotlib
* numpy
* pyserial

Install dependencies using:

```bash id="c1f7mq"
pip install -r requirements.txt
```

---

## Running the Dashboard

Open a terminal in the project folder and run:

```bash id="r8d3tp"
streamlit run software/dashboard/wind_tunnel_dashboard.py
```

The dashboard will automatically open in your web browser.

Default address:

```text id="9j6p2v"
http://localhost:8501
```

---

## Serial Connection Setup

Before starting the dashboard:

1. Connect Arduino to the computer using USB
2. Upload the firmware to Arduino
3. Identify the serial port

Example ports:

Mac:

```text id="6t2k5p"
/dev/cu.usbmodemXXXX
```

Linux / Raspberry Pi:

```text id="2k7x8f"
/dev/ttyACM0
```

Windows:

```text id="5p9z1r"
COM3
```

---

## Starting Data Logging

Steps:

1. Select the correct serial port
2. Set baud rate to 9600
3. Click **Start Logging**
4. Run the wind tunnel experiment

The dashboard will begin displaying live data.

---

## Generated Outputs

The system automatically produces:

CSV data file

Graphs:

* Lift vs Time
* Drag vs Time
* CL vs CD

Download options:

* CSV file
* Graph images

---

## Troubleshooting

No data visible:

Check Arduino connection

Verify serial port

Confirm baud rate is 9600

Ensure sensors are powered

---

## Purpose

The dashboard provides a simple and reliable interface for monitoring aerodynamic behavior in real time and recording experimental data for analysis.
