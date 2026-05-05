import csv
import io
import math
import os
import re
import time
import zipfile
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import serial
import streamlit as st
from serial.tools import list_ports


CSV_COLUMNS = [
    "Timestamp",
    "Elapsed_s",
    "Temperature_C",
    "Pressure_Pa",
    "AirSpeed_mps",
    "Lift_g",
    "Drag_g",
    "Density_kgm3",
    "DynamicPressure_Pa",
    "ReynoldsNumber",
    "DynamicRange_mps",
    "CL",
    "CD",
    "CLCD_Ratio",
]

R_AIR = 287.05
G_TO_NEWTON = 0.00980665


def init_state() -> None:
    if "running" not in st.session_state:
        st.session_state.running = False
    if "ser" not in st.session_state:
        st.session_state.ser = None
    if "csv_file" not in st.session_state:
        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        st.session_state.csv_file = f"wind_tunnel_log_{stamp}.csv"
    if "start_time" not in st.session_state:
        st.session_state.start_time = None
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=CSV_COLUMNS)
    if "last_sensor" not in st.session_state:
        st.session_state.last_sensor = {
            "lift": float("nan"),
            "drag": float("nan"),
            "pressure": float("nan"),
            "temperature": float("nan"),
            "speed": float("nan"),
        }
    if "last_raw_line" not in st.session_state:
        st.session_state.last_raw_line = ""
    if "parse_fail_count" not in st.session_state:
        st.session_state.parse_fail_count = 0
    if "serial_buffer" not in st.session_state:
        st.session_state.serial_buffer = ""
    if "bytes_read_count" not in st.session_state:
        st.session_state.bytes_read_count = 0
    if "serial_ready_at" not in st.session_state:
        st.session_state.serial_ready_at = 0.0


def ensure_csv(path: str) -> None:
    if os.path.exists(path):
        return
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_COLUMNS)


def parse_line(line: str) -> dict[str, float] | None:
    values: dict[str, float] = {}
    # Accept forms like key:1.23 or key=1.23 separated by comma/space/semicolon.
    pairs = re.findall(
        r"([A-Za-z_]+)\s*[:=]\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)",
        line,
    )
    for key, val in pairs:
        key = key.strip().lower()
        try:
            values[key] = float(val)
        except ValueError:
            continue

    # Also accept plain numeric CSV style: lift,drag,pressure,temperature,speed
    if not values:
        parts = [p.strip() for p in re.split(r"[,;\s]+", line) if p.strip()]
        if len(parts) >= 5:
            try:
                nums = [float(parts[i]) for i in range(5)]
                return {
                    "lift": nums[0],
                    "drag": nums[1],
                    "pressure": nums[2],
                    "temperature": nums[3],
                    "speed": nums[4],
                }
            except ValueError:
                pass

    aliases = {
        "lift": ["lift", "lift_g", "l"],
        "drag": ["drag", "drag_g", "d"],
        "pressure": ["pressure", "pressure_pa", "p"],
        "temperature": ["temperature", "temp", "temperature_c", "t"],
        "speed": ["speed", "airspeed", "speed_mps", "s", "v", "velocity"],
    }

    out: dict[str, float] = {}
    for target, keys in aliases.items():
        for k in keys:
            if k in values:
                out[target] = values[k]
                break

    if not out:
        return None
    return out


def air_viscosity_pa_s(temp_c: float) -> float:
    temp_k = temp_c + 273.15
    c = 110.4
    mu0 = 1.716e-5
    t0 = 273.15
    return mu0 * ((temp_k / t0) ** 1.5) * ((t0 + c) / (temp_k + c))


def append_row(parsed: dict[str, float], area_m2: float, char_len_m: float, dyn_range_window: int) -> None:
    now = datetime.now()

    if st.session_state.start_time is None:
        st.session_state.start_time = now
    elapsed = (now - st.session_state.start_time).total_seconds()

    temp_c = parsed.get("temperature", float("nan"))
    pressure_pa = parsed.get("pressure", float("nan"))
    speed_mps = parsed.get("speed", float("nan"))
    lift_g = parsed.get("lift", float("nan"))
    drag_g = parsed.get("drag", float("nan"))

    temp_k = temp_c + 273.15 if not math.isnan(temp_c) else float("nan")
    density = (
        pressure_pa / (R_AIR * temp_k)
        if (not math.isnan(pressure_pa) and not math.isnan(temp_k) and temp_k > 0)
        else float("nan")
    )
    q = (
        0.5 * density * speed_mps * speed_mps
        if (not math.isnan(density) and not math.isnan(speed_mps))
        else float("nan")
    )
    mu = air_viscosity_pa_s(temp_c) if not math.isnan(temp_c) else float("nan")
    reynolds = (
        density * speed_mps * char_len_m / mu
        if (not math.isnan(density) and not math.isnan(speed_mps) and not math.isnan(mu) and mu > 0)
        else float("nan")
    )

    lift_n = lift_g * G_TO_NEWTON
    drag_n = drag_g * G_TO_NEWTON

    denom = q * area_m2 if not math.isnan(q) else float("nan")
    cl = (lift_n / denom) if (not math.isnan(denom) and denom > 0) else float("nan")
    cd = (drag_n / denom) if (not math.isnan(denom) and denom > 0) else float("nan")
    clcd = (cl / cd) if (not math.isnan(cl) and not math.isnan(cd) and cd != 0) else float("nan")

    new_row = {
        "Timestamp": now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "Elapsed_s": elapsed,
        "Temperature_C": temp_c,
        "Pressure_Pa": pressure_pa,
        "AirSpeed_mps": speed_mps,
        "Lift_g": lift_g,
        "Drag_g": drag_g,
        "Density_kgm3": density,
        "DynamicPressure_Pa": q,
        "ReynoldsNumber": reynolds,
        "DynamicRange_mps": float("nan"),
        "CL": cl,
        "CD": cd,
        "CLCD_Ratio": clcd,
    }

    st.session_state.df = pd.concat(
        [st.session_state.df, pd.DataFrame([new_row])], ignore_index=True
    )

    if len(st.session_state.df) > 0:
        dr = (
            st.session_state.df["AirSpeed_mps"]
            .rolling(window=dyn_range_window, min_periods=1)
            .apply(lambda s: float(s.max() - s.min()), raw=False)
        )
        st.session_state.df["DynamicRange_mps"] = dr


def flush_latest_rows_to_csv(csv_path: str, old_len: int) -> None:
    latest = st.session_state.df.iloc[old_len:]
    if latest.empty:
        return
    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        for _, row in latest.iterrows():
            writer.writerow([row[col] for col in CSV_COLUMNS])


def close_serial() -> None:
    ser = st.session_state.ser
    if ser is not None:
        try:
            ser.close()
        except Exception:
            pass
    st.session_state.ser = None


def apply_theme_css(theme: str) -> None:
    background = "#0e1117"
    surface = "#161b22"
    text = "#f0f3f6"
    muted = "#a8b3c1"
    border = "rgba(255, 255, 255, 0.12)"
    card = "rgba(22, 27, 34, 0.94)"

    st.markdown(
        f"""
        <style>
            .stApp {{
                background: {background};
                color: {text};
            }}
            [data-testid="stHeader"] {{
                background: {background};
            }}
            section[data-testid="stSidebar"] {{
                background: {surface};
            }}
            .block-container {{
                padding-top: 1.2rem;
                padding-bottom: 2rem;
            }}
            div[data-testid="stMetric"] {{
                background: {card};
                border: 1px solid {border};
                border-radius: 16px;
                padding: 0.8rem 1rem;
            }}
            div[data-testid="stMetricLabel"] {{
                color: {muted};
            }}
            div[data-testid="stDataFrame"] {{
                border: 1px solid {border};
                border-radius: 16px;
                overflow: hidden;
            }}
            .frame-shell {{
                border: 1px solid {border};
                border-radius: 18px;
                padding: 1rem;
                background: {card};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _line_plot_png(df: pd.DataFrame, x: str, y: str, title: str, ylabel: str) -> bytes:
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df[x], df[y], linewidth=1.8)
    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.35)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    return buf.getvalue()


def _multi_line_plot_png(df: pd.DataFrame, x: str, ys: list[str], title: str, ylabel: str) -> bytes:
    fig, ax = plt.subplots(figsize=(10, 4))
    for y in ys:
        ax.plot(df[x], df[y], linewidth=1.8, label=y)
    ax.set_title(title)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.35)
    ax.legend()
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    return buf.getvalue()


def _scatter_plot_png(df: pd.DataFrame, x: str, y: str, title: str, xlabel: str, ylabel: str) -> bytes:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(df[x], df[y], s=14, alpha=0.75)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.35)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    return buf.getvalue()


def build_graph_zip(df: pd.DataFrame) -> bytes:
    out = io.BytesIO()
    with zipfile.ZipFile(out, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "01_lift_vs_time.png",
            _line_plot_png(df, "Elapsed_s", "Lift_g", "Lift vs Time", "Lift (g)"),
        )
        zf.writestr(
            "02_drag_vs_time.png",
            _line_plot_png(df, "Elapsed_s", "Drag_g", "Drag vs Time", "Drag (g)"),
        )
        zf.writestr(
            "03_cl_cd_line.png",
            _multi_line_plot_png(df, "Elapsed_s", ["CL", "CD"], "CL vs CD", "Coefficient"),
        )
    return out.getvalue()


st.set_page_config(page_title="Wind Tunnel Dashboard", layout="wide")
init_state()

st.title("Wind Tunnel Live Dashboard")

available_ports = [p.device for p in list_ports.comports()]
default_port = next(
    (p.device for p in list_ports.comports() if getattr(p, "vid", None) == 9025),
    "/dev/ttyACM0" if "/dev/ttyACM0" in available_ports else (available_ports[0] if available_ports else "/dev/ttyAMA10"),
)
if default_port not in available_ports:
    available_ports = [default_port] + available_ports

st.sidebar.header("Serial")
port = st.sidebar.selectbox(
    "Serial Port",
    options=available_ports,
    index=available_ports.index(default_port) if default_port in available_ports else 0,
    placeholder="Connect device to see ports",
)
baud_rate = st.sidebar.number_input(
    "Baud Rate",
    min_value=300,
    max_value=2000000,
    value=9600,
    step=300,
)

st.sidebar.header("Model Inputs")
apply_theme_css("Dark")

reference_area_m2 = st.sidebar.number_input(
    "Reference Area A (m^2)", min_value=0.000001, value=0.01, format="%.6f"
)
characteristic_length_m = st.sidebar.number_input(
    "Characteristic Length L (m)", min_value=0.000001, value=0.10, format="%.6f"
)
dyn_range_window = st.sidebar.number_input(
    "Dynamic Range Window (samples)", min_value=2, max_value=500, value=20, step=1
)
samples_per_refresh = st.sidebar.number_input(
    "Samples per refresh", min_value=1, max_value=200, value=20, step=1
)
refresh_sec = st.sidebar.number_input(
    "Refresh interval (sec)", min_value=0.1, max_value=5.0, value=0.5, step=0.1
)

csv_file = st.session_state.csv_file
ensure_csv(csv_file)

if st.session_state.df.empty and os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
    try:
        st.session_state.df = pd.read_csv(csv_file)
    except Exception:
        st.session_state.df = pd.DataFrame(columns=CSV_COLUMNS)

col_a, col_b, col_c = st.columns(3)
with col_a:
    if st.button("Start Logging", type="primary"):
        if not port:
            st.error("No serial port found. Connect your device and select a port.")
        else:
            st.session_state.running = True

with col_b:
    if st.button("Stop Logging"):
        st.session_state.running = False
        close_serial()

with col_c:
    if st.button("Clear Session Data"):
        st.session_state.df = pd.DataFrame(columns=CSV_COLUMNS)
        st.session_state.start_time = None
        close_serial()
        with open(csv_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_COLUMNS)

if st.session_state.running and st.session_state.ser is None:
    try:
        st.session_state.ser = serial.Serial(port, int(baud_rate), timeout=0.1)
        if st.session_state.start_time is None:
            st.session_state.start_time = datetime.now()
        st.session_state.serial_ready_at = time.monotonic() + 2.5
        time.sleep(1.0)
    except Exception as e:
        st.session_state.running = False
        close_serial()
        st.error(f"Serial error: {e}")

if st.session_state.running and st.session_state.ser is not None:
    before_len = len(st.session_state.df)
    new_samples = 0
    read_deadline = time.monotonic() + max(1.0, float(refresh_sec) * 2.0)
    while time.monotonic() < read_deadline and new_samples < int(samples_per_refresh):
        try:
            if time.monotonic() < st.session_state.serial_ready_at:
                time.sleep(0.05)
                continue

            waiting = st.session_state.ser.in_waiting
            packet = st.session_state.ser.read(waiting if waiting > 0 else 256)
            if not packet:
                time.sleep(0.05)
                continue
            st.session_state.bytes_read_count += len(packet)
            chunk = packet.decode(errors="ignore").replace("\r", "\n")
            st.session_state.serial_buffer += chunk

            lines = st.session_state.serial_buffer.split("\n")
            st.session_state.serial_buffer = lines.pop() if lines else ""

            for raw_line in lines:
                raw = raw_line.strip()
                if not raw:
                    continue
                if raw.lower().startswith("started arduino"):
                    continue
                parsed = parse_line(raw)
                if parsed is None:
                    if any(tag in raw.lower() for tag in ("l:", "d:", "p:", "t:", "s:")):
                        st.session_state.parse_fail_count += 1
                    continue
                st.session_state.last_raw_line = raw
                st.session_state.last_sensor.update(parsed)
                append_row(
                    st.session_state.last_sensor,
                    reference_area_m2,
                    characteristic_length_m,
                    int(dyn_range_window),
                )
                new_samples += 1
                if new_samples >= int(samples_per_refresh):
                    break
        except Exception:
            continue
    flush_latest_rows_to_csv(csv_file, before_len)

st.markdown("### Live Values")

if not st.session_state.df.empty:
    last = st.session_state.df.iloc[-1]
    m1, m2, m3, m4, m5, m6, m7 = st.columns(7)
    m1.metric("Lift (g)", f"{last['Lift_g']:.2f} g")
    m2.metric("Drag (g)", f"{last['Drag_g']:.2f} g")
    m3.metric("CL", f"{last['CL']:.4f}")
    m4.metric("CD", f"{last['CD']:.4f}")
    m5.metric("Air speed (m/s)", f"{last['AirSpeed_mps']:.2f} m/s")
    m6.metric("Temperature (°C)", f"{last['Temperature_C']:.2f} °C")
    m7.metric("Pressure (Pa)", f"{last['Pressure_Pa']:.2f} Pa")
else:
    st.info("No data yet. Click Start Logging after selecting the correct serial port.")

df_plot = st.session_state.df.copy()

if st.session_state.running:
    if st.session_state.bytes_read_count == 0:
        st.caption("Waiting for serial bytes from the device.")
    elif df_plot.empty:
        st.caption(f"Waiting for first parseable sensor frame. Last sensor line: {st.session_state.last_raw_line}")

st.divider()
st.markdown("### Required Graphs")

if not df_plot.empty:
    chart_col1, chart_col2, chart_col3 = st.columns(3)
    with chart_col1:
        st.subheader("Lift vs Time")
        st.line_chart(df_plot.set_index("Elapsed_s")["Lift_g"])

    with chart_col2:
        st.subheader("Drag vs Time")
        st.line_chart(df_plot.set_index("Elapsed_s")["Drag_g"])

    with chart_col3:
        st.subheader("CL vs CD")
        st.line_chart(df_plot.set_index("Elapsed_s")[["CL", "CD"]])

st.divider()
st.markdown("### Live CSV Reading Data")
with st.container(border=True):
    st.dataframe(df_plot, use_container_width=True)

csv_bytes = df_plot.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download CSV",
    data=csv_bytes,
    file_name=csv_file,
    mime="text/csv",
)

if not df_plot.empty:
    graph_zip = build_graph_zip(df_plot)
    st.download_button(
        "Download All Graphs (PNG ZIP)",
        data=graph_zip,
        file_name="wind_tunnel_graphs.zip",
        mime="application/zip",
    )

if st.session_state.running:
    time.sleep(float(refresh_sec))
    st.rerun()