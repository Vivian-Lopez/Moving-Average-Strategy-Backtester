import sys, os, subprocess

# Add C++ module path
so_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../build/strategy_py.so"))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../build")))

# If strategy_py.so does not exist, run CMake and make
if not os.path.exists(so_path):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(this_dir, ".."))

    build_dir = os.path.join(repo_root, "build")
    os.makedirs(build_dir, exist_ok=True)

    subprocess.run(["cmake", repo_root], cwd=build_dir, check=True)
    subprocess.run(["make"], cwd=build_dir, check=True)

import strategy_py
import pandas as pd

def run_simulation(csv_path, short_window=3, long_window=5):
    pnl_curve, total_profit = strategy_py.run_strategy(csv_path, short_window, long_window)
    df = pd.read_csv(csv_path, header=None, names=["Timestamp", "Close"])
    df['PnL'] = pnl_curve
    return df, total_profit