#include "strategy.hpp"

// Defining the constructore for the class which was declared in the header file here
MomentumStrategy::MomentumStrategy(int short_window, int long_window) 
    : short_window_(short_window),
        long_window_(long_window),
        short_sum_(0.0),
        long_sum_(0.0),
        tick_index_(0)
{
    short_window_buffer_.reserve(short_window);
    long_window_buffer_.reserve(long_window);
}

int MomentumStrategy::on_price(double price) {
    ++tick_index_;
    
    short_sum_ += price;
    short_window_buffer_.push_back(price);
    if (short_window_buffer_.size() > short_window_) {
        short_sum_ -= short_window_buffer_[0];
        short_window_buffer_.erase(short_window_buffer_.begin());
    }
    
    long_sum_ += price;
    long_window_buffer_.push_back(price);
    if (long_window_buffer_.size() > long_window_) {
        long_sum_ -= long_window_buffer_[0];
        long_window_buffer_.erase(long_window_buffer_.begin());
    }

    if (long_window_buffer_.size() == long_window_) {
        double short_ma = short_sum_ / short_window_;
        double long_ma = long_sum_ / long_window_;
        return short_ma > long_ma ? 1 : (short_ma < long_ma ? - 1 : 0);
    }
    
    return 0;
}