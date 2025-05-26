#include "strategy.hpp"
#include <iostream>

std::vector<int> generate_signals(const std::vector<double> &prices, int short_window, int long_window)
{
    std::vector<int> signals(prices.size(), 0);
    double short_sum = 0.0;
    double long_sum = 0.0;

    for (auto i = 0; i < prices.size(); ++i)
    {
        short_sum += prices[i];
        if (i >= short_window)
        {
            short_sum -= prices[i - short_window];
        }

        long_sum += prices[i];
        if (i >= long_window)
        {
            long_sum -= prices[i - long_window];
        }

        if (i >= long_window - 1)
        {
            double short_ma = short_sum / short_window;
            double long_ma = long_sum / long_window;
            signals[i] = short_ma > long_ma ? 1 : (short_ma < long_ma ? -1 : 0);
        }
    }

    return signals;
}
