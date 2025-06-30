#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "strategy.hpp"
#include "csv_loader.hpp"
#include <chrono>

namespace py = pybind11;

auto run_strategy(const std::string filepath, int short_window, int long_window)
{
    auto start_total = std::chrono::high_resolution_clock::now();
    MomentumStrategy strategy(short_window, long_window);
    std::vector<double> pnl_curve;
    double profit = 0.0;
    int shares = 0;
    double avg_entry = 0.0;
    double last_price = 0.0;

    double on_price_us = 0.0;
    int on_price_calls = 0;
    load_prices_from_csv(filepath, [&](double price)
                         {
        auto t1 = std::chrono::high_resolution_clock::now();
        int signal = strategy.on_price(price);
        auto t2 = std::chrono::high_resolution_clock::now();
        on_price_us += std::chrono::duration<double, std::micro>(t2 - t1).count();
        ++on_price_calls;
        if (signal == 1) {
            if (shares >= 0) {
                avg_entry = ((avg_entry * shares) + price) / (shares + 1);
                ++shares;
            } else {
                double closed_val = avg_entry * -shares - price * -shares;
                profit += closed_val;
                shares = 0;
                avg_entry = 0;
            }
        } else if (signal == -1) {
            if (shares <= 0) {
                avg_entry = ((avg_entry * -shares) + price) / (-shares + 1);
                --shares;
            } else {
                double closed_val = price * shares - avg_entry * shares;
                profit += closed_val;
                avg_entry = 0;
                shares = 0;
            }
        }
        pnl_curve.push_back(profit);
        last_price = price; });
    double avg_on_price_us = on_price_calls > 0 ? on_price_us / on_price_calls : 0.0;

    if (shares > 0)
        profit += (last_price - avg_entry) * shares;
    else if (shares < 0)
        profit += (avg_entry - last_price) * -shares;

    auto end_total = std::chrono::high_resolution_clock::now();
    double total_ms = std::chrono::duration<double, std::milli>(end_total - start_total).count();

    return std::make_tuple(pnl_curve, profit, avg_on_price_us, total_ms);
}

PYBIND11_MODULE(strategy_py, m)
{
    m.def("run_strategy", &run_strategy, "Run the strategy on CSV data", py::arg("filepath"),
          py::arg("short_window"), py::arg("long_window"));
}