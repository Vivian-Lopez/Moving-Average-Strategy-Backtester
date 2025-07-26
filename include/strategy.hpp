#pragma once

#include "circular_buffer.hpp"

class MomentumStrategy {
public:
    MomentumStrategy(int short_window, int long_window);

    // Accepts the next price, returns signal
    int on_price(double price);

private:
    CircularBuffer<double> short_window_buffer_;
    CircularBuffer<double> long_window_buffer_;
};
