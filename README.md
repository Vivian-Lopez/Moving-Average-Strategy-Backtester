# 📉 Moving Average Strategy Backtester (C++20 & Python)

A **performance-focused** implementation of a moving average crossover strategy and backtester, designed for **low-latency trading infrastructure** experimentation.

Key design pillars:

- ⚡ High-performance signal generation in **modern C++20**
- 🔁 Seamless integration with **Python** (Streamlit) for visualization and control

🔗 **Try the live demo**: [Streamlit App](https://trading-strategy-simulator-cpp.streamlit.app/)

---

## 📸 Current UI

![Light UI](https://github.com/user-attachments/assets/e08cfbf9-9334-43fe-8e38-6cf9ce5b3094)  
![Light UI 2](https://github.com/user-attachments/assets/91ba8ab1-8d1a-4e68-9203-4f7bb3822b95)

> *(Dark mode coming soon)*

---

## 🚀 Project Highlights

- **Optimized core logic** from ~0.30µs to **0.09µs** latency using a **rolling average** and **circular buffer** in C++20
- **Modular architecture** for fast signal prototyping and large-scale backtests
- Supports **Python-driven simulation** and future integration with tick-level data feeds

---

## 📈 Strategy Logic

A simple **SMA crossover** strategy:

- **Buy (+1)**: Short MA crosses above long MA  
- **Sell (-1)**: Short MA crosses below  
- **Hold (0)**: No crossover

Designed to serve as a base for more complex signal generation.

---

## 🧱 Project Structure

```
moving-average-strategy-cpp/
├── src/         # Low-latency core logic (C++20)
├── include/     # Headers and abstractions
├── python/      # Streamlit frontend & glue logic
├── data/        # Sample CSV price data
├── tests/       # C++ unit tests (Google Test)
```

---

## 🧪 Testing

Unit tests validate:

- Proper signal generation on crossover
- Edge cases: flat/rising/falling markets
- Output length/structure consistency

---

## 🔬 Performance & Optimization Roadmap

- ⏱️ Integrate **Google Benchmark** for microprofiling  
- 🧵 Add **OpenMP / TBB** for vectorized strategy eval  
- ⚙️ Build **event-based backtest engine** with slippage modeling  

---

## 🛠 Build & Run

### Requirements

- C++20 with concepts support, CMake ≥ 3.16  
- Python 3, Streamlit  
- GoogleTest (`brew install googletest`)

### Run (compiles on the fly)

```bash
cd ./python
streamlit run app.py
```

