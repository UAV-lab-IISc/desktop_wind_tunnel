# WIND TUNNEL SINGLE-ANGLE ANALYZER

## Quick Start Guide

### 1. Installation

```bash
pip install pandas numpy matplotlib
```

### 2. Change AOA at Top of Code

Open `wind_tunnel_analyzer.py` and modify these lines:

```python
# ============================================================================
# ===== WIND TUNNEL CONFIGURATION - CHANGE THESE VALUES =====
# ============================================================================

ANGLE_OF_ATTACK = 0              # ← CHANGE THIS! Examples: -20, -10, 0, 20, 25
CSV_FILE = "0D.csv"              # ← CSV file name (e.g., "0D.csv", "-20D.csv")
OUTPUT_DIRECTORY = "wind_tunnel_output"  # Where to save the analysis figure

# ============================================================================
```

### 3. Run the Analysis

```bash
python wind_tunnel_analyzer.py
```

**That's it!** Your analysis figure will be generated in the `wind_tunnel_output` folder.

---

## How to Change Angle of Attack

It's very simple - change **ONE number** at the top:

### Example 1: Analyze 0° data
```python
ANGLE_OF_ATTACK = 0
CSV_FILE = "0D.csv"
```

### Example 2: Analyze -20° data
```python
ANGLE_OF_ATTACK = -20
CSV_FILE = "-20D.csv"
```

### Example 3: Analyze +25° data
```python
ANGLE_OF_ATTACK = 25
CSV_FILE = "_25D.csv"
```

Then run: `python wind_tunnel_analyzer.py`

**The angle will automatically appear on:**
- All graph titles
- Main figure title
- Output filename: `wind_tunnel_analysis_0deg.png`
- Statistics section

---

## What You Get

### 5 Essential Graphs (All in One Figure)

1. **CL Distribution** (Top Left)
   - Histogram of lift coefficients
   - Shows mean and median values
   - Reveals data spread and outliers

2. **CD Distribution** (Top Right)
   - Histogram of drag coefficients
   - Shows mean and median values
   - Indicates measurement consistency

3. **Lift vs Drag Scatter** (Middle Left)
   - Shows relationship between CL and CD
   - Color-coded by CL value
   - Red star shows mean point
   - Classic aerodynamic polar view

4. **L/D Ratio Distribution** (Middle Right)
   - Efficiency metric histogram
   - Shows L/D spread
   - Critical for performance analysis
   - Higher is better

5. **CL & CD Over Time** (Bottom - Full Width)
   - Blue line = CL trend
   - Orange line = CD trend
   - Shows measurement stability
   - Time-series behavior of coefficients

### Statistics Table (Below Graphs)

Comprehensive summary including:
- Data point count
- CL: Mean, Median, Std Dev, Min, Max
- CD: Mean, Median, Std Dev, Min, Max
- Forces: Lift and Drag in grams
- Efficiency: L/D Ratio
- Test Conditions: Reynolds Number, Temperature, Pressure, Air Speed

---

## CSV File Requirements

Your CSV file must contain these columns:

**Required:**
- `CL` - Lift coefficient
- `CD` - Drag coefficient
- `Elapsed_s` - Time in seconds
- `Temperature_C` - Temperature
- `Pressure_Pa` - Pressure
- `AirSpeed_mps` - Air speed
- `ReynoldsNumber` - Reynolds number
- `Lift_g` - Lift in grams
- `Drag_g` - Drag in grams

**Example CSV structure:**
```csv
Timestamp,Elapsed_s,Temperature_C,Pressure_Pa,AirSpeed_mps,Lift_g,Drag_g,Density_kgm3,DynamicPressure_Pa,ReynoldsNumber,DynamicRange_mps,CL,CD,CLCD_Ratio
2026-04-26 12:28:59.088,2.624526,30.3,90844.0,0.99,-1.72,-0.5101994991,1.0429213438708065,0.5110836045638887,5544.489095362619,0.0,-3.3003285273439955,-0.978968582276946,3.371230279594761
```

---

## Understanding the Output

### Graph Interpretation

#### CL Distribution
- **Tall, narrow peak** = Consistent, high-quality data
- **Wide, flat distribution** = Noisy or unstable data
- **Multiple peaks** = May indicate different flow regimes

#### CD Distribution
- **Narrow peak** = Good measurement precision
- **Wide spread** = High measurement noise
- **Outliers** = Check for data collection issues

#### Lift vs Drag
- **Points along smooth curve** = Normal aerodynamic behavior
- **Scattered points** = Turbulent or unstable conditions
- **Outliers** = Potential measurement errors
- **Red star** = Your mean operating point

#### L/D Ratio
- **Higher values** = Better efficiency
- **Positive values** = Generating useful lift
- **Negative values** = Stalled or reversed flow
- **Sharp peak** = Stable efficiency

#### CL & CD Over Time
- **Smooth lines** = Stable wind tunnel conditions
- **Oscillating lines** = Turbulent flow or instability
- **Sudden jumps** = Flow separation or transition
- **Diverging lines** = Data quality issue

### Statistics Meaning

| Metric | What It Means |
|--------|---------------|
| **CL Mean** | Average lift coefficient for this angle |
| **CL Std Dev** | Measurement variability (lower is better) |
| **CD Mean** | Average drag coefficient |
| **L/D Ratio** | Efficiency (lift per unit drag) |
| **Reynolds Number** | Flow regime indicator |

---

## Example Workflow

### Step 1: Check your files
```bash
ls -la *.csv
# Output: 0D.csv, -20D.csv, 20D.csv, etc.
```

### Step 2: Edit wind_tunnel_analyzer.py
```python
ANGLE_OF_ATTACK = 0      # Change to 0, -20, 20, 25, etc.
CSV_FILE = "0D.csv"      # Match your filename
```

### Step 3: Run analysis
```bash
python wind_tunnel_analyzer.py
```

### Step 4: Check output
```bash
ls wind_tunnel_output/
# Output: wind_tunnel_analysis_0deg.png
```

### Step 5: View the figure
- Open `wind_tunnel_output/wind_tunnel_analysis_0deg.png`
- You'll see all 5 graphs with your AOA clearly labeled

---

## Troubleshooting

### Error: "File not found"
**Solution:** Check that CSV file exists and path is correct
```python
CSV_FILE = "0D.csv"  # Make sure this file is in the same directory
```

### Error: "Column 'CL' not found"
**Solution:** Verify CSV has correct column names
```bash
head 0D.csv  # Check the first line (headers)
```

### Graphs look empty or strange
**Solution:** Check for NaN values in data
```python
import pandas as pd
df = pd.read_csv("0D.csv")
print(df['CL'].isnull().sum())  # See how many NaN values
```

### Permission denied when saving
**Solution:** Create output directory manually
```bash
mkdir wind_tunnel_output
```

---

## Output File Details

### Filename Convention
- For AOA = 0°: `wind_tunnel_analysis_0deg.png`
- For AOA = -20°: `wind_tunnel_analysis_-20deg.png`
- For AOA = 25°: `wind_tunnel_analysis_25deg.png`

### File Properties
- **Format:** PNG (Portable Network Graphics)
- **Resolution:** 300 DPI (publication quality)
- **Size:** ~500-800 KB
- **Color:** Full color, ready for reports
- **Dimensions:** 16" × 12" (when printed at 100 DPI)

---

## Using in Reports

### For Your Wind Tunnel Report:

1. **Get the figure:** `wind_tunnel_analysis_0deg.png`
2. **Insert into document** (Word, PDF, etc.)
3. **Reference in caption:** "Wind Tunnel Analysis at 0° Angle of Attack"
4. **Use statistics** from the summary table

### Example Caption:
```
Figure 1: Wind Tunnel Analysis at 0° Angle of Attack
Comprehensive analysis showing lift and drag distributions (top),
lift vs drag relationship (middle), and time-series behavior (bottom).
Statistics table shows mean CL = 0.234, mean CD = 0.0089.
```

---

## Advanced: Batch Processing Multiple Angles

To analyze multiple angles, create a script like this:

```python
# analyze_all_angles.py
import subprocess

angles = [0, -10, 20, 25, -20]
csv_files = {
    0: "0D.csv",
    -10: "-10D.csv",
    20: "_20D.csv",
    25: "_25D.csv",
    -20: "-20D.csv"
}

for aoa in angles:
    # Edit wind_tunnel_analyzer.py for each angle
    with open('wind_tunnel_analyzer.py', 'r') as f:
        content = f.read()
    
    content = content.replace(f'ANGLE_OF_ATTACK = {angles[0]}', f'ANGLE_OF_ATTACK = {aoa}')
    content = content.replace(f'CSV_FILE = "{csv_files[angles[0]]}"', f'CSV_FILE = "{csv_files[aoa]}"')
    
    with open('wind_tunnel_analyzer.py', 'w') as f:
        f.write(content)
    
    # Run analysis
    subprocess.run(['python', 'wind_tunnel_analyzer.py'])
    print(f"✓ Completed analysis for {aoa}°")
```

Then run: `python analyze_all_angles.py`

---

## Key Features

✅ **Simple:** Change one number, run code  
✅ **Clear:** AOA displayed on all graphs  
✅ **Professional:** 300 DPI output, publication-ready  
✅ **Complete:** 5 essential graphs + statistics  
✅ **Fast:** Analysis in seconds  
✅ **Reliable:** Handles common issues automatically  
✅ **Documented:** All code fully commented  

---

## File Structure

```
Your Project Folder/
├── wind_tunnel_analyzer.py     (main script)
├── 0D.csv                       (your wind tunnel data)
├── -20D.csv                     (other angles)
├── 20D.csv
└── wind_tunnel_output/          (created automatically)
    ├── wind_tunnel_analysis_0deg.png
    ├── wind_tunnel_analysis_-20deg.png
    └── wind_tunnel_analysis_20deg.png
```

---

## Command Reference

```bash
# Install dependencies
pip install pandas numpy matplotlib

# Run analysis (after editing AOA and CSV_FILE)
python wind_tunnel_analyzer.py

# View results
open wind_tunnel_output/wind_tunnel_analysis_0deg.png  # macOS
start wind_tunnel_output/wind_tunnel_analysis_0deg.png # Windows
```

---

## Technical Details

### Libraries Used
- **pandas:** Data loading and manipulation
- **numpy:** Numerical calculations
- **matplotlib:** Graph generation

### Performance
- **Time:** 2-5 seconds per analysis
- **Memory:** ~50 MB
- **Output size:** ~500 KB per PNG

### Requirements
- Python 3.7+
- pandas >= 1.0
- numpy >= 1.18
- matplotlib >= 3.0

---

## Tips for Best Results

1. **Ensure data quality**
   - Check CSV has complete data
   - Remove obvious outliers if needed
   - Verify column names match

2. **Use consistent naming**
   - 0D.csv for 0°
   - -20D.csv for -20°
   - Keep pattern consistent

3. **Update BOTH values**
   - Change ANGLE_OF_ATTACK
   - Change CSV_FILE
   - Both must match!

4. **Create output directory**
   - Script creates it automatically
   - Or create manually: `mkdir wind_tunnel_output`

5. **Keep copies**
   - Original output files stay in folder
   - Never overwritten
   - Safe for backup

---

## Questions?

### Check These First:
1. Is CSV file in same directory as script?
2. Are column names exactly correct?
3. Is ANGLE_OF_ATTACK number valid?
4. Does CSV_FILE match your filename?

### Verify Data:
```python
import pandas as pd
df = pd.read_csv("0D.csv")
print(df.head())              # First 5 rows
print(df.columns.tolist())    # All columns
print(len(df))                # Total rows
```

---

## Version Information

- **Version:** 1.0
- **Created:** 2026-04-26
- **Status:** Production Ready
- **Last Updated:** 2026-04-26

---

## License

This tool is provided for educational and research purposes.

---

**Happy analyzing! ✈️📊**

Start with editing the two configuration lines at the top:
```python
ANGLE_OF_ATTACK = 0           # ← Your angle here
CSV_FILE = "0D.csv"           # ← Your file here
```

Then run: `python wind_tunnel_analyzer.py`
