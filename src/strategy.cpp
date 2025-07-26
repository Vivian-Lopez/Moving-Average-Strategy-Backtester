// strategy.cpp - MomentumStrategy implementation
#include "strategy.hpp"

MomentumStrategy::MomentumStrategy(int short_window, int long_window) 
    : short_window_buffer_(short_window),
        long_window_buffer_(long_window)
{
}

int MomentumStrategy::on_price(double price) {
    short_window_buffer_.push(price);
    long_window_buffer_.push(price);

    if (long_window_buffer_.is_full()) {
        double short_ma = short_window_buffer_.average();
        double long_ma = long_window_buffer_.average();
        return short_ma > long_ma ? 1 : (short_ma < long_ma ? - 1 : 0);
    }
    
    return 0;
}