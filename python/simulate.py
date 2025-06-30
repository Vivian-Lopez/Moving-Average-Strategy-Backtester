import os
import sys
import subprocess

# Absolute path to expected .so
so_path = os.path.join(os.path.dirname(__file__), "strategy_py.so")

# Build if it doesn't exist
if not os.path.exists(so_path):
    print("🔧 Building strategy_py.so...")
    build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "build"))
    os.makedirs(build_dir, exist_ok=True)
    subprocess.run(["cmake", ".."], cwd=build_dir, check=True)
    subprocess.run(["make"], cwd=build_dir, check=True)

# Add path and import
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import strategy_py
import pandas as pd

def run_simulation(csv_path, short_window=3, long_window=5):
    pnl_curve, total_profit, avg_on_price_us, total_us = strategy_py.run_strategy(csv_path, short_window, long_window)
    df = pd.read_csv(csv_path)
    df['PnL'] = pnl_curve
    return df, total_profit, avg_on_price_us, total_us
