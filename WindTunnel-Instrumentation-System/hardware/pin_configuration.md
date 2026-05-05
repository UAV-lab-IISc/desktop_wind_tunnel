# Pin Configuration

## Wind Tunnel Instrumentation System

### Arduino UNO Sensor and Interface Connections

---

## Overview

This document defines the complete pin configuration for the wind tunnel instrumentation system.
It specifies how each sensor and module is connected to the Arduino UNO microcontroller.

The system uses:

* Two load cells for lift and drag measurement
* HX711 amplifiers for signal conditioning
* Pitot tube pressure sensor for airspeed measurement
* BMP180 environmental sensor for temperature and pressure
* OLED display for real-time visualization

All connections are designed for stable operation, minimal noise, and reliable data acquisition.

---

# Digital Pin Assignments

## Load Cell 1 — Lift Measurement

HX711 Module (Lift Channel)

| Signal      | HX711 Pin | Arduino UNO Pin | Function             |
| ----------- | --------- | --------------- | -------------------- |
| Data Output | DT        | D2              | Lift load cell data  |
| Clock       | SCK       | D3              | Lift load cell clock |

---

## Load Cell 2 — Drag Measurement

HX711 Module (Drag Channel)

| Signal      | HX711 Pin | Arduino UNO Pin | Function             |
| ----------- | --------- | --------------- | -------------------- |
| Data Output | DT        | D4              | Drag load cell data  |
| Clock       | SCK       | D5              | Drag load cell clock |

---

# Analog Pin Assignments

## Differential Pressure Sensor — Airspeed Measurement

| Signal          | Device          | Arduino UNO Pin | Function                    |
| --------------- | --------------- | --------------- | --------------------------- |
| Pressure Output | Pitot / MPX2010 | A0              | Differential pressure input |

---

# I²C Bus Connections

The I²C communication bus allows multiple devices to share the same communication lines.

Devices connected:

* BMP180 Temperature and Pressure Sensor
* OLED Display

---

## I²C Pin Mapping

| Signal | Device       | Arduino UNO Pin | Description  |
| ------ | ------------ | --------------- | ------------ |
| SDA    | BMP180, OLED | A4              | Serial Data  |
| SCL    | BMP180, OLED | A5              | Serial Clock |

---

## I²C Device Addresses

| Device        | Address |
| ------------- | ------- |
| BMP180 Sensor | 0x77    |
| OLED Display  | 0x3C    |

---

# Power Connections

All modules share a common power supply and ground reference.

| Component       | Voltage | Connection       |
| --------------- | ------- | ---------------- |
| Arduino UNO     | 5 V     | USB power        |
| HX711 Modules   | 5 V     | 5V rail          |
| Load Cells      | 5 V     | HX711 module     |
| Pressure Sensor | 5 V     | 5V rail          |
| BMP180 Sensor   | 3.3 V   | Arduino 3.3V pin |
| OLED Display    | 5 V     | 5V rail          |

---

# Ground Connections

All components must share a common ground.

Connect:

Arduino GND → HX711 GND
Arduino GND → Pressure Sensor GND
Arduino GND → BMP180 GND
Arduino GND → OLED GND

This ensures stable signal reference and prevents measurement errors.

---

# Wiring Summary

Lift Load Cell:

DT → D2
SCK → D3

Drag Load Cell:

DT → D4
SCK → D5

Pressure Sensor:

Output → A0

I²C Devices:

SDA → A4
SCL → A5

Power:

5V → All modules
GND → Common ground

---

# Notes

* Always verify wiring before powering the system
* Use short wires to reduce electrical noise
* Ensure secure connections to avoid signal fluctuations
* Perform calibration after wiring changes
