"""
PROFESSIONAL WIND TUNNEL ANALYSIS TOOL - NACA 0012 AIRFOIL
IEEE STYLE REPORT WITH DETAILED GRAPH EXPLANATIONS
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# WIND TUNNEL CONFIGURATION
# ============================================================================

ANGLE_OF_ATTACK = -10  # Change this! Examples: -20, -10, 0, 20, 25
CSV_FILE = "-10D .csv"  # CSV file name
OUTPUT_DIRECTORY = "wind_tunnel_output"
FIXED_AIR_SPEED = 6.87  # Fixed air speed (m/s)


# ============================================================================


class WindTunnelAnalyzer:
    """Professional wind tunnel analyzer with IEEE-style reporting"""

    def __init__(self, csv_filepath, angle_of_attack, output_dir="wind_tunnel_output"):
        self.csv_filepath = csv_filepath
        self.aoa = angle_of_attack
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.df = None

        plt.style.use('seaborn-v0_8-whitegrid')
        plt.rcParams['figure.figsize'] = (16, 18)
        plt.rcParams['font.size'] = 10
        plt.rcParams['font.family'] = 'sans-serif'

    def load_data(self):
        """Load CSV data"""
        try:
            self.df = pd.read_csv(self.csv_filepath)
            print(f"✓ Data loaded: {self.csv_filepath}")
            print(f"  Rows: {self.df.shape[0]}, Columns: {self.df.shape[1]}\n")
            return True
        except Exception as e:
            print(f"✗ Error: {e}")
            return False

    def get_statistics(self):
        """Calculate statistics"""
        df_clean = self.df.dropna(subset=['CL', 'CD'])

        stats = {
            'data_points': len(df_clean),
            'cl_mean': df_clean['CL'].mean(),
            'cl_median': df_clean['CL'].median(),
            'cl_std': df_clean['CL'].std(),
            'cl_min': df_clean['CL'].min(),
            'cl_max': df_clean['CL'].max(),
            'cd_mean': df_clean['CD'].mean(),
            'cd_median': df_clean['CD'].median(),
            'cd_std': df_clean['CD'].std(),
            'cd_min': df_clean['CD'].min(),
            'cd_max': df_clean['CD'].max(),
            'lift_mean': df_clean['Lift_g'].mean(),
            'lift_std': df_clean['Lift_g'].std(),
            'drag_mean': df_clean['Drag_g'].mean(),
            'drag_std': df_clean['Drag_g'].std(),
            'ld_ratio': df_clean['CL'].mean() / df_clean['CD'].mean() if df_clean['CD'].mean() != 0 else 0,
            'reynolds': df_clean['ReynoldsNumber'].mean(),
            'temperature': df_clean['Temperature_C'].mean(),
            'pressure': df_clean['Pressure_Pa'].mean(),
            'airspeed': FIXED_AIR_SPEED,
        }
        return stats

    def create_ieee_style_figure(self):
        """Create IEEE-style professional figure with all elements"""

        stats = self.get_statistics()
        df_clean = self.df.dropna(subset=['CL', 'CD'])

        # Create main figure with title area - more compact
        fig = plt.figure(figsize=(16, 18))

        # ====================================================================
        # MAIN ANALYSIS AREA (No header box - goes below)
        # ====================================================================

        # GridSpec for graphs - more compact
        gs = gridspec.GridSpec(5, 2, figure=fig,
                               hspace=0.55, wspace=0.35,
                               top=0.98, bottom=0.15, left=0.08, right=0.92)

        # ====================================================================
        # GRAPH 1: CL Distribution (Top Left)
        # ====================================================================
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.hist(df_clean['CL'], bins=30, color='#1f77b4', alpha=0.7, edgecolor='black', linewidth=1.2)
        ax1.axvline(stats['cl_mean'], color='red', linestyle='--', linewidth=2.5,
                    label=f"Mean: {stats['cl_mean']:.4f}")
        ax1.axvline(stats['cl_median'], color='green', linestyle='--', linewidth=2,
                    label=f"Median: {stats['cl_median']:.4f}")
        ax1.set_xlabel('Lift Coefficient (CL)', fontweight='bold', fontsize=10)
        ax1.set_ylabel('Frequency', fontweight='bold', fontsize=10)
        ax1.set_title(f'(a) CL Distribution at AOA: {self.aoa}°',
                      fontweight='bold', fontsize=11, loc='left')
        ax1.legend(fontsize=8, loc='upper right')
        ax1.grid(True, alpha=0.3, linestyle='--')

        # ====================================================================
        # GRAPH 2: CD Distribution (Top Right)
        # ====================================================================
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.hist(df_clean['CD'], bins=30, color='#ff7f0e', alpha=0.7, edgecolor='black', linewidth=1.2)
        ax2.axvline(stats['cd_mean'], color='red', linestyle='--', linewidth=2.5,
                    label=f"Mean: {stats['cd_mean']:.4f}")
        ax2.axvline(stats['cd_median'], color='green', linestyle='--', linewidth=2,
                    label=f"Median: {stats['cd_median']:.4f}")
        ax2.set_xlabel('Drag Coefficient (CD)', fontweight='bold', fontsize=10)
        ax2.set_ylabel('Frequency', fontweight='bold', fontsize=10)
        ax2.set_title(f'(b) CD Distribution at AOA: {self.aoa}°',
                      fontweight='bold', fontsize=11, loc='left')
        ax2.legend(fontsize=8, loc='upper right')
        ax2.grid(True, alpha=0.3, linestyle='--')

        # ====================================================================
        # GRAPH 3: Lift vs Drag Scatter (Row 2 Left)
        # ====================================================================
        ax3 = fig.add_subplot(gs[1, 0])
        scatter = ax3.scatter(df_clean['CD'], df_clean['CL'],
                              c=df_clean['CL'], cmap='viridis',
                              s=50, alpha=0.6, edgecolors='black', linewidth=0.8)
        ax3.scatter(stats['cd_mean'], stats['cl_mean'], color='red', s=350,
                    marker='*', edgecolors='darkred', linewidth=2,
                    label='Mean Point', zorder=5)
        ax3.set_xlabel('Drag Coefficient (CD)', fontweight='bold', fontsize=10)
        ax3.set_ylabel('Lift Coefficient (CL)', fontweight='bold', fontsize=10)
        ax3.set_title(f'(c) Aerodynamic Polar (CL vs CD) at AOA: {self.aoa}°',
                      fontweight='bold', fontsize=11, loc='left')
        ax3.legend(fontsize=8, loc='best')
        ax3.grid(True, alpha=0.3, linestyle='--')
        cbar = plt.colorbar(scatter, ax=ax3, label='CL Value', shrink=0.7)
        cbar.ax.tick_params(labelsize=8)

        # ====================================================================
        # GRAPH 4: L/D Ratio Distribution (Row 2 Right)
        # ====================================================================
        ax4 = fig.add_subplot(gs[1, 1])
        ld_ratio = df_clean['CL'] / df_clean['CD'].replace(0, np.nan)
        ld_ratio = ld_ratio.dropna()
        ax4.hist(ld_ratio, bins=30, color='#2ca02c', alpha=0.7, edgecolor='black', linewidth=1.2)
        ax4.axvline(stats['ld_ratio'], color='red', linestyle='--', linewidth=2.5,
                    label=f"Mean L/D: {stats['ld_ratio']:.2f}")
        ax4.set_xlabel('Lift-to-Drag Ratio (L/D)', fontweight='bold', fontsize=10)
        ax4.set_ylabel('Frequency', fontweight='bold', fontsize=10)
        ax4.set_title(f'(d) Efficiency Ratio (L/D) Distribution at AOA: {self.aoa}°',
                      fontweight='bold', fontsize=11, loc='left')
        ax4.legend(fontsize=8, loc='upper right')
        ax4.grid(True, alpha=0.3, linestyle='--')

        # ====================================================================
        # GRAPH 5: CL & CD Over Time (Row 3 - Full Width)
        # ====================================================================
        ax5 = fig.add_subplot(gs[2, :])
        ax5_twin = ax5.twinx()

        elapsed_time = df_clean['Elapsed_s'].values
        cl_values = df_clean['CL'].values
        cd_values = df_clean['CD'].values

        line1 = ax5.plot(elapsed_time, cl_values, color='#1f77b4', linewidth=2.5,
                         marker='o', markersize=3, label='CL', alpha=0.8)
        line2 = ax5_twin.plot(elapsed_time, cd_values, color='#ff7f0e', linewidth=2.5,
                              marker='s', markersize=3, label='CD', alpha=0.8)

        ax5.set_xlabel('Elapsed Time (seconds)', fontweight='bold', fontsize=10)
        ax5.set_ylabel('Lift Coefficient (CL)', fontweight='bold', fontsize=10, color='#1f77b4')
        ax5_twin.set_ylabel('Drag Coefficient (CD)', fontweight='bold', fontsize=10, color='#ff7f0e')
        ax5.set_title(f'(e) Time-Series Analysis: CL and CD Variation at AOA: {self.aoa}°',
                      fontweight='bold', fontsize=11, loc='left')

        ax5.tick_params(axis='y', labelcolor='#1f77b4', labelsize=9)
        ax5_twin.tick_params(axis='y', labelcolor='#ff7f0e', labelsize=9)
        ax5.grid(True, alpha=0.3, linestyle='--')

        # Combine legends
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax5.legend(lines, labels, loc='upper left', fontsize=9, framealpha=0.95)

        # ====================================================================
        # HEADER + EXPLANATIONS + STATISTICS (Row 4-5 - Combined)
        # ====================================================================

        header_text = (
            "NACA 0012 SYMMETRIC AIRFOIL - Aerodynamic Characteristics Analysis\n"
            "Indian Institute of Science (IISC) Bangalore \n"
            " Department of Aerospace Engineering\n "
            " MAV Laboratory\n"
            "Guidance: Dr. S.N.Omkar\n"
            "Authors: K A Advayee | Ravikath | Saakshi | Muruli SS"
        )

        explanation_text = (
            f"TEST CONDITIONS: AOA: {self.aoa}° | Air Speed: {FIXED_AIR_SPEED} m/s | Re: {stats['reynolds']:.0f} | Temp: {stats['temperature']:.1f}°C | Pressure: {stats['pressure']:.0f} Pa\n"
            f"DATA: CL = {stats['cl_mean']:.4f} ± {stats['cl_std']:.4f} | CD = {stats['cd_mean']:.4f} ± {stats['cd_std']:.4f} | L/D = {stats['ld_ratio']:.2f} | Points: {stats['data_points']}\n\n"
            f"GRAPH EXPLANATIONS:\n"
            f"(a) CL Distribution: Shows frequency of lift coefficient measurements. Narrow bell-shaped distribution indicates stable, high-quality measurements. Mean and median close together suggest low data skewness.\n"
            f"(b) CD Distribution: Represents drag coefficient variability. Narrow distribution indicates precise force balance measurements with minimal turbulence. Std dev reflects measurement precision.\n"
            f"(c) Polar Plot: Shows relationship between lift and drag. Each point is a measurement. Curve reveals aerodynamic efficiency trade-offs. Red star = mean operating point.\n"
            f"(d) L/D Ratio: Primary efficiency metric in aerospace. Higher L/D indicates better performance for cruise flight. Distribution width reflects variability due to flow fluctuations.\n"
            f"(e) Time-Series: Reveals measurement stability. CL (blue) and CD (orange) should show minimal drift. Stable lines indicate good experimental conditions."
        )

        ax_combined = fig.add_subplot(gs[3:, :])
        ax_combined.axis('off')

        # Header at top
        ax_combined.text(0.5, 1.0, header_text, transform=ax_combined.transAxes,
                         ha='center', va='top', fontsize=9, fontweight='bold',
                         bbox=dict(boxstyle='round,pad=0.6', facecolor='lightblue',
                                   edgecolor='navy', linewidth=1.5))

        # Explanations below header
        ax_combined.text(0.02, 0.75, explanation_text, transform=ax_combined.transAxes,
                         ha='left', va='top', fontsize=8, family='sans-serif',
                         bbox=dict(boxstyle='round,pad=0.7', facecolor='lightyellow',
                                   edgecolor='orange', linewidth=1.5, alpha=0.9))

        # College block - compact, bottom right
        college_text = (
            "IISC\nAero Dept\nMAV Lab"
        )
        ax_combined.text(0.98, 0.05, college_text, transform=ax_combined.transAxes,
                         ha='right', va='bottom', fontsize=8, fontweight='bold',
                         bbox=dict(boxstyle='round,pad=0.4', facecolor='lightgray',
                                   edgecolor='black', linewidth=1))

        return fig, stats

    def save_figure(self, fig):
        """Save figure to file"""
        filename = f"NACA_0012_Analysis_{self.aoa}deg.png"
        filepath = self.output_dir / filename
        fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ report saved: {filepath}\n")
        return str(filepath)

    def run_analysis(self):
        """Run complete analysis"""
        print("\n" + "=" * 80)
        print(" WIND TUNNEL ANALYSIS")
        print("NACA 0012 AIRFOIL - MAV LABORATORY, IISC BANGALORE")
        print("=" * 80)
        print(f"\nConfiguration:")
        print(f"  Airfoil Model: NACA 0012 (Symmetric)")
        print(f"  Angle of Attack: {self.aoa}°")
        print(f"  CSV Data File: {self.csv_filepath}")
        print(f"  Fixed Air Speed: {FIXED_AIR_SPEED} m/s")
        print(f"  Output Directory: {self.output_dir}\n")

        if not self.load_data():
            return False

        print("Generating report figure...")
        fig, stats = self.create_ieee_style_figure()

        output_file = self.save_figure(fig)
        plt.close(fig)

        print("=" * 80)
        print("ANALYSIS COMPLETE - REPORT GENERATED")
        print("=" * 80)
        print(f"\nKey Aerodynamic Metrics (AOA: {self.aoa}°):")
        print(f"  • CL (Lift Coefficient):      {stats['cl_mean']:>10.6f}")
        print(f"  • CD (Drag Coefficient):      {stats['cd_mean']:>10.6f}")
        print(f"  • L/D Ratio (Efficiency):     {stats['ld_ratio']:>10.4f}")
        print(f"  • Lift Force (Mean):          {stats['lift_mean']:>10.6f} g")
        print(f"  • Drag Force (Mean):          {stats['drag_mean']:>10.6f} g")
        print(f"  • Reynolds Number:            {stats['reynolds']:>10.2f}")
        print(f"\nTest Conditions:")
        print(f"  • Temperature:                {stats['temperature']:>10.2f}°C")
        print(f"  • Atmospheric Pressure:      {stats['pressure']:>10.1f} Pa")
        print(f"  • Air Speed:                  {FIXED_AIR_SPEED:>10.2f} m/s")
        print(f"  • Total Data Points:          {stats['data_points']:>10}")
        print(f"\nReport Output File: {output_file}")
        print("=" * 80 + "\n")

        return True


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    analyzer = WindTunnelAnalyzer(
        csv_filepath=CSV_FILE,
        angle_of_attack=ANGLE_OF_ATTACK,
        output_dir=OUTPUT_DIRECTORY
    )

    analyzer.run_analysis()