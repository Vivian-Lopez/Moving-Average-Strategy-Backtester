#include <iostream>
#include "strategy.hpp"
#include "csv_loader.hpp"

int main()
{
    MomentumStrategy strategy(3, 5);

    double profit = 0.0;
    int position = 0; // 1 for long, -1 for short, 0 for flat
    double entry_price = 0.0;
    double last_price = 0.0;

    // For each price, feeds price to strategy.on_price(price) and handle signals:
    //    - If signal == 1 and not already long, enter long (close short if needed)
    //    - If signal == -1 and not already short, enter short (close long if needed)
    //    - If signal == 0, hold position
    load_prices_from_csv("../data/sample_data.csv", [&](double price)
                         {
        last_price = price;
        int signal = strategy.on_price(price);
        if (signal == 1 && position != 1) {
            // Close short position if exists
            if (position == -1) {
                profit += entry_price - price;
            }
            position = 1;
            entry_price = price;
        } else if (signal == -1 && position != -1) {
            if (position == 1) {
                profit += price - entry_price;
            }
            position = -1;
            entry_price = price;
        } });

    // Closing any open position at the last price
    if (position == 1)
    {
        profit += last_price - entry_price;
    }
    else if (position == -1)
    {
        profit += entry_price - last_price;
    }

    std::cout << "Total profit: " << profit << std::endl;
    return 0;
}
