#pragma once
#include <vector>

class CircularBuffer {
public:
    // Constructor: initialize buffer with a fixed capacity
    CircularBuffer(size_t capacity);

    // Add a new value to the buffer (replace oldest if full)
    void push(double value);

    // Check if the buffer is full
    bool is_full() const;

    // Get the current average of values in the buffer
    double average() const;

private:
    std::vector<double> data_;  // The internal data storage
    size_t capacity_;           // Max number of elements
    size_t start_;              // Index of the oldest element
    size_t size_;               // Current number of elements
    double sum_;                // Running sum for average
};