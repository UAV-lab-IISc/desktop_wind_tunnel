# Arduino Firmware Guide

## Wind Tunnel Data Acquisition System

### Arduino UNO Sensor Interface and Control Program

---

## Overview

This firmware runs on the Arduino UNO and performs real-time data acquisition from the wind tunnel instrumentation system.

The Arduino reads sensor data from:

* Lift load cell
* Drag load cell
* Pitot tube (airspeed)
* BMP sensor (temperature and pressure)

The firmware processes the sensor readings and sends formatted data to the Raspberry Pi or computer through serial communication for visualization and logging.

---

## Sensors Connected

Lift Load Cell
Drag Load Cell
Pitot Tube Pressure Sensor
BMP Temperature and Pressure Sensor
OLED Display

---

## Pin Configuration Summary

Lift Load Cell:

DT → D2
SCK → D3

Drag Load Cell:

DT → D4
SCK → D5

I²C Devices:

SDA → A4
SCL → A5

Power:

5 V → All modules
GND → Common ground

---

## Required Arduino Libraries

Install the following libraries using the Arduino Library Manager:

HX711

Adafruit BMP085 / BMP180

Adafruit GFX

Adafruit SSD1306

Wire

---

## Installing Libraries

Open:

Arduino IDE

Then:

Sketch → Include Library → Manage Libraries

Search and install:

HX711
Adafruit BMP085
Adafruit GFX
Adafruit SSD1306

---

## Uploading the Firmware

Steps:

1. Connect Arduino UNO to the computer using USB
2. Open Arduino IDE
3. Open file:

```text id="n7p3r8"
wind_tunnel_uno.ino
```

4. Select board:

Arduino UNO

5. Select port:

Tools → Port

6. Click:

Upload

---

## Serial Communication Settings

Baud Rate:

9600

This must match the dashboard configuration.

---

## Firmware Function

The firmware performs the following operations:

Reads load cell values
Calculates force measurements
Reads airspeed from Pitot tube
Reads temperature and pressure
Updates OLED display
Sends sensor data via serial communication

---

## Output Data Format

The Arduino sends data in structured format:

Example:

```text id="x5q1p9"
l:0.03,d:0.00,p:90657,t:31.3,s:0.78
```

Where:

l = Lift (grams)
d = Drag (grams)
p = Pressure (Pa)
t = Temperature (°C)
s = Airspeed (m/s)

---

## Sampling Rate

Typical sampling rate:

1 sample per second (1 Hz)

---

## Notes

Always calibrate load cells before testing

Verify wiring before powering system

Ensure stable mounting of sensors

Use correct serial port

---

## Purpose

This firmware provides reliable real-time data acquisition for aerodynamic testing in the wind tunnel and enables visualization of airflow behavior through the dashboard interface.
