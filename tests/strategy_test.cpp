#include <gtest/gtest.h>
#include "strategy.hpp"

TEST(MomentumStrategyTest, GeneratesCorrectSignalsForRisingPrices)
{
    std::vector<double> prices = {100, 101, 102, 103, 104, 105, 106};
    int short_window = 3;
    int long_window = 5;

    auto signals = generate_signals(prices, short_window, long_window);

    // Expect vector of same size
    EXPECT_EQ(signals.size(), prices.size());

    // Check that signals start at 0 for padding
    for (int i = 0; i < long_window - 1; ++i)
    {
        EXPECT_EQ(signals[i], 0);
    }

    // Check at least one positive and negative signal (assuming crossover)
    bool has_buy = false, has_sell = false;
    for (int i = long_window; i < prices.size(); ++i)
    {
        if (signals[i] == 1)
            has_buy = true;
        if (signals[i] == -1)
            has_sell = true;
    }

    EXPECT_TRUE(has_buy || has_sell);
}

TEST(MomentumStrategyTest, GeneratesCorrectSignalsForConstantPrices)
{
    std::vector<double> prices = {100, 100, 100, 100, 100, 100, 100};
    int short_window = 3;
    int long_window = 5;
    auto signals = generate_signals(prices, short_window, long_window);

    EXPECT_EQ(signals.size(), prices.size());
    EXPECT_EQ(signals, std::vector<int>(prices.size(), 0));
}

TEST(MomentumStrategyTest, GeneratesCorrectSignals)
{
    auto prices = std::vector<double>{100, 102, 101, 104, 106, 105, 107, 110, 112};
    int short_window = 3;
    int long_window = 5;

    auto signals = generate_signals(prices, short_window, long_window);
    auto expected_signals = std::vector<int>{0, 0, 0, 0, 1, 1, 1, 1, 1};

    EXPECT_EQ(signals, expected_signals);
}