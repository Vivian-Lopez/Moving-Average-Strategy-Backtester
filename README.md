# Momentum-Strategy-Optimization-C++

An educational and performance-aware C++ implementation of a simple momentum-based trading strategy, structured for further development in:

- ✅ Signal generation and testing  
- ✅ Backtesting and analytics integration  
- ✅ Profiling and low-level optimization


Try out the live version here: https://trading-strategy-simulator-cpp.streamlit.app/

Frontend created with the Python Streamlit framework.

# The Current UI:
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/d3b7f85d-4b09-4abc-977f-67677f54c6ec" />

---

## 🚀 Project Goals

This repo serves as a foundation to explore:

- Implementation of fast, clean signal-generation logic in modern C++
- Integration with Python for data visualization and analysis
- Optimization of compute bottlenecks for large-scale backtests
- Practical demonstration of production-grade design in a trading context

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

### Build

```bash
mkdir build && cd build
cmake ..
make
```

### Run

```bash
./momentum_strategy
./strategy_test  # Run unit tests
```

---

## 🧪 Tests

Unit tests in `tests/strategy_test.cpp` validate:

- Correct signal vector sizing and alignment
- Proper handling of flat and rising markets
- Signal generation at crossover points
- Structure for backtesting tests (coming soon)

---

## 🔬 Optimization Plan

- ⏱️ **Benchmarking**: Integrate [Google Benchmark](https://github.com/google/benchmark) to measure performance  
- 🧠 **Profiling**: Use `Instruments`, `perf`, or `valgrind` to analyze hotspots  
- 🧵 **Multithreading**: Apply OpenMP or Intel TBB for large vector parallelism  
- 🧪 **Backtesting engine**: Build an event-based framework with slippage modeling  
- 📊 **Python bridge**: Export signals to Python for matplotlib-based visualization  

---

## 📌 Planned Features

The following extensions are planned or in progress:

- [ ] Full backtesting module (PnL tracking, execution logic)
- [ ] CSV loader for real historical data
- [ ] Parameter sweeps for signal window optimization
- [ ] Micro-benchmarking hooks and timing utilities
- [ ] Python scripts for plotting and performance visualization
- [ ] Parallelized backtest/strategy evaluation
