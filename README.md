# Moving-Average-Strategy-Backtester

A performance-aware Python and C++ implementation of a simple moving average trading strategy as well as backtesting app, structured for further development in:

- Signal generation and testing  
- Backtesting and analytics integration  
- Profiling and low-level optimization

Try out the live version here: https://trading-strategy-simulator-cpp.streamlit.app/

# The Current UI:
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/e08cfbf9-9334-43fe-8e38-6cf9ce5b3094" />
<img width="1438" alt="image" src="https://github.com/user-attachments/assets/91ba8ab1-8d1a-4e68-9203-4f7bb3822b95" />
(Enhanced Dark Mode coming soon)

---

## 🚀 Project Goals

This repo serves as a foundation to explore:

- Implementation of fast, clean signal-generation logic in modern C++
- Integration with Python for data visualization and analysis
- Optimization of compute bottlenecks for large-scale backtests

---

## 📈 Strategy Overview

The core strategy uses a **simple moving average (SMA) crossover** technique:

- **Buy Signal (+1)**: Short MA crosses above Long MA  
- **Sell Signal (-1)**: Short MA crosses below Long MA  
- **Hold (0)**: Otherwise

Signals are generated from historical price vectors and can be used to simulate trading strategies.

---

## 📁 Project Structure

```
momentum-strategy-optimization-cpp/
├── data/            # Sample price data (CSV)
├── include/         # Strategy function declarations (headers)
├── python/          # Streamlit frontend and simulation code 
├── src/             # Core strategy logic (C++)
├── tests/           # Unit tests using Google Test
├── CMakeLists.txt   # Build system definition
├── README.md        # You're reading it
```

---

## 🛠️ Build Instructions

### Requirements

- C++17 or later
- CMake ≥ 3.16
- GoogleTest (`brew install googletest` on macOS)
- Python3
- Streamlit

### Run (Build is done dynamicaly during run in simulate.py)

```bash
cd ./python
streamlit run app.py
```

---

## 🧪 Tests

Unit tests in `tests/strategy_test.cpp` validate:

- Correct signal vector sizing and alignment
- Proper handling of flat and rising markets
- Signal generation at crossover points

---

## 🔬 Optimization Plan

- ⏱️ **Benchmarking**: Integrate [Google Benchmark](https://github.com/google/benchmark) to measure performance  
- 🧵 **Multithreading**: Apply OpenMP or Intel TBB for large vector parallelism  
- 🧪 **Backtesting engine**: Build an event-based framework with slippage modeling  

---

## 📌 Planned Features

The following extensions are planned or in progress:
- [ ] Parallelized backtest/strategy evaluation
- [ ] Realtime connection and visualisation to frontend tick-by-tick
