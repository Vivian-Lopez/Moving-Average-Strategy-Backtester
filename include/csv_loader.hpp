#pragma once

#include <string>
#include <functional>

void load_prices_from_csv(const std::string& filepath, const std::function<void(double)>& callback);