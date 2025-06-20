#include "csv_loader.hpp"
#include <fstream>
#include <sstream>
#include <iostream>

void load_prices_from_csv(const std::string& filepath, const std::function<void(double)>& callback) {
    std::ifstream file(filepath);
    if (!file.is_open()) {
        std::cerr << "Failed to open sample csv file" << std::endl;
    }

    std::string line;
    while (std::getline(file, line)) {

        std::istringstream iss(line);
        std::string token;
        if (!std::getline(iss, token, ',')) continue;
        std::string timestamp = token;

        if (!std::getline(iss, token, ',')) continue;

        double price;
        try {
            price = std::stod(token);
            callback(price);
        } catch (const std::invalid_argument& e) {
            std::cout << "invalid argument" << std::endl;
        } catch (const std::out_of_range& e) {
            std::cout << "out of range for double" << std::endl;
        }
    }
}