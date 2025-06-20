#include <gtest/gtest.h>
#include "strategy.hpp"

TEST(MomentumStrategyTest, GeneratesSignalsOneByOne)
{
    MomentumStrategy strategy(3, 5);
    auto prices = std::vector<double>{100, 102, 101, 104, 106, 105, 107, 110, 112};
    auto expectedSignals = std::vector<int>{0, 0, 0, 0, 1, 1, 1, 1, 1};

    for (int i = 0; i < prices.size(); ++i)
    {
        auto signal = strategy.on_price(prices[i]);
        EXPECT_DOUBLE_EQ(signal, expectedSignals[i]);
    }
}