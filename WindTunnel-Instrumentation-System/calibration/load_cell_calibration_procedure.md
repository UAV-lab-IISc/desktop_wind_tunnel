# Load Cell Calibration Procedure

## Wind Tunnel Instrumentation System

### Calibration of Lift and Drag Force Measurement Sensors

---

## Overview

This document describes the calibration procedure used to convert raw load cell readings into accurate force measurements for the wind tunnel instrumentation system.

The system uses two independent load cells arranged in an L-shaped configuration to measure:

* Lift force (vertical direction)
* Drag force (horizontal direction)

Calibration ensures that the measured electrical signals from the load cells correspond accurately to known physical forces. Proper calibration is essential for obtaining reliable aerodynamic data during wind tunnel testing.

---

# Purpose of Calibration

The objective of calibration is to:

* Establish the relationship between sensor output and applied force
* Convert raw sensor readings into grams-force (gf)
* Ensure measurement accuracy
* Maintain repeatability between experiments
* Reduce measurement error

Calibration is performed before experimental testing or whenever the mechanical setup is modified.

---

# Equipment Required

Calibration weights (1 g to 100 g)
Load cell mounting structure
Digital scale (optional)
Stable mounting platform
Data acquisition system (Arduino + HX711)
Computer with serial monitor or dashboard

---

# Load Cell Configuration

Lift Load Cell:

Measures vertical aerodynamic force acting on the airfoil.

Drag Load Cell:

Measures horizontal aerodynamic force opposing airflow.

Configuration Type:

Orthogonal L-shaped load cell arrangement.

This configuration allows independent measurement of lift and drag forces without mechanical interference.

---

# Calibration Principle

Load cells operate based on strain gauge deformation.

Applied Force → Mechanical Deformation → Electrical Signal → Digital Output

The relationship between force and sensor output is linear within the operating range.

The calibration equation is:

Force (grams) = (Sensor Reading − Offset) / Calibration Factor

---

# Calibration Steps

## Step 1 — System Setup

Ensure the load cell structure is securely mounted.

Verify all wiring connections.

Power the system.

Allow sensors to stabilize for 1 to 2 minutes.

---

## Step 2 — Tare (Zero Calibration)

Place the airfoil model and mounting structure in position.

Do not apply any external weight.

Record the baseline reading.

This value is the zero offset.

Example:

Zero Offset = 8388000 counts

---

## Step 3 — Apply Known Weights

Place known calibration weights on the load cell.

Apply weights incrementally.

Recommended sequence:

10 g
20 g
30 g
50 g
75 g
100 g

Allow 2 to 3 seconds for the reading to stabilize before recording each value.

---

## Step 4 — Record Calibration Data

Create a calibration table.

| Applied Weight (g) | Sensor Reading (counts) |
| ------------------ | ----------------------- |
| 0                  | 8388000                 |
| 10                 | 8408500                 |
| 20                 | 8429000                 |
| 30                 | 8449500                 |
| 50                 | 8490500                 |
| 75                 | 8541500                 |
| 100                | 8592500                 |

---

## Step 5 — Calculate Calibration Factor

Use linear regression to determine the slope.

Calibration Factor:

Counts per gram

Example:

Calibration Factor = 2050 counts per gram

---

## Step 6 — Update Firmware

Insert the calibration factor into the Arduino code.

Example:

```cpp
float CALIB_FACTOR = 2050.0;
```

Upload the updated firmware to the Arduino.

---

## Step 7 — Verification

Apply a known weight.

Compare measured value with actual value.

Acceptable error:

±0.5 grams

Repeat measurement at least three times.

---

# Calibration Frequency

Calibration should be performed:

Before each experiment session
After hardware modification
After sensor replacement
If measurement accuracy changes

---

# Accuracy and Performance

Measurement Range:

0 to 100 grams

Resolution:

0.1 gram

Expected Accuracy:

±0.5 gram

Repeatability:

Better than 0.1 gram

Linearity:

Greater than 99.9 percent

---

# Important Notes

Ensure the load cell is not overloaded.

Avoid sudden impact on the load cell.

Use stable mounting during calibration.

Keep the load direction consistent.

Perform calibration in a vibration-free environment.

---

# Example Calibration Result

Lift Load Cell:

Sensitivity:

2050 counts per gram

Zero Offset:

8388000 counts

Measurement Range:

0 to 100 grams

---

Drag Load Cell:

Sensitivity:

2048 counts per gram

Zero Offset:

8389000 counts

Measurement Range:

0 to 100 grams

---

# Conclusion

The load cell calibration procedure establishes a reliable relationship between applied force and sensor output. Accurate calibration ensures that lift and drag measurements reflect true aerodynamic forces acting on the airfoil during wind tunnel testing.

Proper calibration is essential for generating meaningful aerodynamic data, validating experimental results, and maintaining measurement consistency across multiple test sessions.
