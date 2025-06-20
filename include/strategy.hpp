#pragma once

#include <vector>

class MomentumStrategy {
public:
    MomentumStrategy(int short_window, int long_window);

    // Accepts the next price, returns signal
    int on_price(double price);

private:
    int short_window_;
    int long_window_;
    std::vector<double> short_window_buffer_;
    std::vector<double> long_window_buffer_;
    double short_sum_;
    double long_sum_;
    int tick_index_;    // Tracks how many prices seen
};