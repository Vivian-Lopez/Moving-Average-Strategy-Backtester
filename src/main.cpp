#include <iostream>
#include "strategy.hpp"
#include "csv_loader.hpp"

int main()
{
    MomentumStrategy strategy(3, 5);

    double profit = 0.0;
    int shares = 0; // can be negative if in a short position
    double average_entry_price = 0.0;
    double last_price = 0.0;

    // For each price, feeds price to strategy.on_price(price) and handle signals:
    //    - If signal == 1 and not already long, enter long (close short if needed)
    //    - If signal == -1 and not already short, enter short (close long if needed)
    //    - If signal == 0, hold position
    load_prices_from_csv("../data/sample_data.csv", [&](double price)
                         {
        int signal = strategy.on_price(price);
        if (signal == 1) {
            // Shares can be negative so use absolute values where necessary
            // Correctly calculate the profit using average entry price and price
            if (shares >= 0) {
                average_entry_price = ((average_entry_price * shares) + price) / (shares + 1);
                ++shares;
            } else {
                // Closing a short position
                double sold_shares_value = average_entry_price * -shares;
                double equivalent_current_shares_value = price * -shares;
                profit += sold_shares_value - equivalent_current_shares_value;
                average_entry_price = 0;
                shares = 0;
            }
        } else if (signal == -1) {
            if (shares < 0) {
                average_entry_price = ((average_entry_price * -shares) + price) / (-shares + 1);
                --shares;
            } else {
                // Closing a long position
                profit += (shares * price) - (average_entry_price * shares);
                average_entry_price = 0;
                shares = 0;
            }
        } 
        last_price = price;
    });

    // Closing any open position at the last price
    if (shares < 0) {
        double sold_shares_value = average_entry_price * -shares;
        double equivalent_current_shares_value = last_price * -shares;
        profit += sold_shares_value - equivalent_current_shares_value;
        average_entry_price = 0;
        shares = 0;
    } else if (shares > 0) {
        profit += (shares * last_price) - (average_entry_price * shares);
        average_entry_price = 0;
        shares = 0;
    }

    std::cout << "Total profit: " << profit << std::endl;
    return 0;
}
