# Momentum-Strategy-Optimization-C++

An educational and performance-aware C++ implementation of a simple momentum-based trading strategy, structured for further development in:

- ✅ Signal generation and testing  
- ✅ Backtesting and analytics integration  
- ✅ Profiling and low-level optimization

---

## 🚀 Project Goals

This repo serves as a foundation to explore:

- Implementation of fast, clean signal-generation logic in modern C++
- Integration with Python for data and visualization (optional)
- Optimization of compute bottlenecks for large-scale backtests
- Practical demonstration of production-like code in a trading context

---

## 📈 Strategy Overview

The core strategy uses a **simple moving average (SMA) crossover** technique:

- **Buy Signal (+1)**: Short MA crosses above Long MA  
- **Sell Signal (-1)**: Short MA crosses below Long MA  
- **Hold (0)**: Otherwise

All signals are generated from historical price vectors.

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

Unit tests are implemented with GoogleTest in `tests/strategy_test.cpp`.  
They check correctness of signal output across edge cases:

- Rising price sequences  
- Constant price sequences  
- Mixed trend reversals  

---

## 🔬 Optimization Plan (Future Work)

- ⏱️ **Benchmarking**: Integrate [Google Benchmark](https://github.com/google/benchmark) to measure performance  
- 🧠 **Profiling**: Use `Instruments`, `perf`, or `valgrind` to analyze hotspots  
- 🧵 **Multithreading**: Apply OpenMP or Intel TBB for large vector parallelism  
- 🧪 **Backtesting engine**: Build an event-based framework with slippage modeling  
- 📊 **Python bridge**: Export signals to Python for matplotlib-based visualization  
