# Power Distribution

## Wind Tunnel Instrumentation System

### Electrical Supply and Power Management for Data Acquisition Platform

---

## Overview

This document describes the electrical power distribution and supply configuration for the subsonic open-air wind tunnel instrumentation system. The system is designed as a low-power embedded measurement platform that operates safely from a regulated 5 V DC supply.

All sensors, signal conditioning modules, and display devices are powered from a common 5 V supply rail provided by the Arduino UNO through a USB connection. This simplified power architecture ensures stable operation, ease of assembly, and reliable performance during experimental testing.

The power distribution design prioritizes:

* Stable voltage supply
* Low electrical noise
* Safe operation
* Reliable sensor measurements
* Simple wiring configuration

---

# Power Source

Primary Supply:

USB Power from Computer or External USB Adapter

Supply Voltage:

5 Volts DC

Minimum Current Capacity:

500 mA

Recommended Current Capacity:

1 A

Typical Operating Current:

Approximately 160 mA

Power Delivery Method:

USB cable connected to Arduino UNO

---

# Power Distribution Architecture

The instrumentation system uses a **single 5 V power rail architecture**, where all components receive power from the Arduino UNO.

Power is distributed using:

* Breadboard power rails
* Jumper wire connections
* Shared ground reference

This configuration simplifies wiring and reduces the risk of voltage mismatch between devices.

---

# Component Power Requirements

| Component                | Supply Voltage | Typical Current | Description                            |
| ------------------------ | -------------- | --------------- | -------------------------------------- |
| Arduino UNO              | 5 V            | 80 mA           | Main control and data acquisition unit |
| HX711 Module — Lift      | 5 V            | 25 mA           | Load cell signal conditioning          |
| HX711 Module — Drag      | 5 V            | 25 mA           | Load cell signal conditioning          |
| Load Cells (Lift & Drag) | 5 V            | negligible      | Passive force sensors                  |
| Pitot Pressure Sensor    | 5 V            | 5 mA            | Airspeed measurement                   |
| BMP180 Sensor Module     | 5 V            | 1 mA            | Temperature and pressure measurement   |
| OLED Display             | 5 V            | 15 mA           | Real-time data display                 |

---

# Total System Current

Estimated Total Current:

160 mA

Safety Margin:

More than 300 mA

Recommended Power Supply:

5 V, 500 mA minimum

Preferred Power Supply:

5 V, 1 A USB adapter

This ensures stable operation even under peak load conditions.

---

# Power Distribution Layout

The system uses a shared power rail configuration.

## 5V Power Line

Arduino 5V → HX711 Lift Module
Arduino 5V → HX711 Drag Module
Arduino 5V → Pitot Pressure Sensor
Arduino 5V → BMP180 Sensor
Arduino 5V → OLED Display

## Ground Line

Arduino GND → HX711 Lift Module
Arduino GND → HX711 Drag Module
Arduino GND → Pitot Pressure Sensor
Arduino GND → BMP180 Sensor
Arduino GND → OLED Display

All devices share a common electrical ground reference.

---

# Voltage Regulation

The Arduino UNO includes internal voltage regulation circuitry that ensures stable power delivery to connected components.

The system relies on:

* USB regulated 5 V supply
* Internal voltage stabilization
* Low current draw components

No external voltage regulator is required for this system configuration.

---

# Power Stability Considerations

To ensure reliable measurements and prevent electrical noise, the following practices are recommended:

Use short and secure power wires
Avoid loose connections
Keep signal wires separated from power wires
Use stable USB power supply
Ensure proper grounding
Verify connections before powering the system

---

# Safety Guidelines

Always disconnect power before modifying wiring

Do not exceed load cell rated capacity

Avoid short circuits between power and ground

Use insulated wiring connections

Check wiring polarity before powering the system

Ensure proper mounting of components

---

# Power Consumption Summary

System Type:

Low-power embedded instrumentation system

Operating Voltage:

5 Volts DC

Typical Current:

160 mA

Maximum Expected Current:

300 mA

Power Source:

USB connection

Power Distribution Method:

Single 5 V shared power rail

---

# Conclusion

The wind tunnel instrumentation system operates using a simple and reliable single-voltage power distribution design. All sensors, signal conditioning modules, and display devices are powered from the Arduino UNO through a regulated 5 V supply. This configuration ensures stable operation, minimal wiring complexity, and safe performance during aerodynamic testing and educational demonstrations.

This power distribution approach is well suited for:

* STEM educational projects
* Wind tunnel instrumentation systems
* Embedded data acquisition platforms
* Low-power experimental setups
