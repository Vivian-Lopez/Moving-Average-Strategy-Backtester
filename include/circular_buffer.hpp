#pragma once
#include <vector>
#include <concepts>

template<typename T>
concept Arithmetic = std::is_arithmetic_v<T>;

template<Arithmetic T>
class CircularBuffer {
public:
    // Constructor: initialize buffer with a fixed capacity
    CircularBuffer(size_t capacity) : data_(capacity), capacity_(capacity), start_(0), size_(0), sum_(0.0) {}

    // Add a new value to the buffer (replace the oldest if full)
    void push(T value) {
        if (is_full()) {
            sum_ -= data_[start_];
        }

        data_[start_] = value;
        sum_ += value;

        start_ = (start_ + 1) % capacity_;

        if (size_ < capacity_) {
            ++size_;
        }
    }

    bool is_full() const {
        return size_ == capacity_;
    }

    double average() const {
        return sum_ / static_cast<double>(size_);
    }

    size_t size() const {
        return size_;
    }

private:
    std::vector<T> data_;       // The internal data storage
    size_t capacity_;           // Max number of elements
    size_t start_;              // Index of the oldest element if full, otherwise next free index
    size_t size_;               // Current number of elements
    T sum_;                     // Running sum for average
};