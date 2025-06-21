#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "strategy.hpp"
#include "csv_loader.hpp"

namespace py = pybind11;

auto run_strategy(const std::string filepath, int short_window, int long_window)
{
    MomentumStrategy strategy(short_window, long_window);
    std::vector<double> pnl_curve;
    double profit = 0.0;
    int shares = 0;
    double avg_entry = 0.0;
    double last_price = 0.0;

    load_prices_from_csv(filepath, [&](double price)
                         {
        int signal = strategy.on_price(price);
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

    if (shares > 0)
        profit += (last_price - avg_entry) * shares;
    else if (shares < 0)
        profit += (avg_entry - last_price) * -shares;

    return std::make_pair(pnl_curve, profit);
}

PYBIND11_MODULE(strategy_py, m)
{
    m.def("run_strategy", &run_strategy, "Run the strategy on CSV data", py::arg("filepath"),
          py::arg("short_window"), py::arg("long_window"));
}