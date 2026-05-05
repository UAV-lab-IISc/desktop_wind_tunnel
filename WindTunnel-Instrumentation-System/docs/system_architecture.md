# System Architecture

## Wind Tunnel Data Acquisition and Visualization System

---

## Overview

The wind tunnel instrumentation system is designed to measure and visualize aerodynamic forces and flow parameters in real time. The system integrates sensors, signal conditioning electronics, a microcontroller, and a visualization dashboard.

The architecture enables continuous measurement of:

* Lift force
* Drag force
* Airspeed
* Temperature
* Pressure

These measurements are processed and displayed as real-time graphs and stored as CSV data for analysis.

---

## System Layers

### 1) Sensor Layer

Responsible for measuring physical quantities inside the wind tunnel.

Components:

* Lift Load Cell (Vertical force)
* Drag Load Cell (Horizontal force)
* Pitot Tube (Airspeed measurement)
* BMP Sensor (Temperature and Pressure)

---

### 2) Signal Conditioning Layer

Converts raw sensor signals into digital values suitable for processing.

Components:

* HX711 Amplifier (Lift)
* HX711 Amplifier (Drag)
* Analog-to-Digital Conversion
* Noise Filtering

---

### 3) Control and Processing Layer

Manages data acquisition and communication.

Component:

* Arduino UNO

Functions:

* Reads sensor data
* Applies calibration
* Sends data via serial communication

---

### 4) Visualization and Logging Layer

Displays data and stores experimental results.

Components:

* Raspberry Pi / PC
* Python Dashboard
* CSV Data Logger

Functions:

* Real-time display
* Graph generation
* Data storage

---

## Data Flow

Sensors
→ HX711 Amplifiers
→ Arduino UNO
→ Serial Communication
→ Dashboard
→ CSV File

---

## Sampling Rate

1 sample per second (1 Hz)

---

## Output Data

The system generates:

* Lift vs Time
* Drag vs Time
* Lift vs Drag
* Coefficient of Lift (CL)
* Coefficient of Drag (CD)
* CL/CD Ratio

---

## Summary

The system architecture provides a simple and reliable framework for real-time aerodynamic measurement and visualization in a subsonic wind tunnel environment.
