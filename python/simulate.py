import strategy_py
import pandas as pd

def run_simulation(csv_path, short_window=3, long_window=5):
    pnl_curve, total_profit = strategy_py.run_strategy(csv_path, short_window, long_window)
    df = pd.read_csv(csv_path, header=None, names=["Timestamp", "Close"])
    df['PnL'] = pnl_curve
    return df, total_profit