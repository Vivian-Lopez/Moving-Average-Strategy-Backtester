cmake_minimum_required(VERSION 3.16)
project(MomentumStrategy)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

add_executable(momentum_strategy
    src/main.cpp
    src/strategy.cpp
    src/csv_loader.cpp
)

# pybind11
include(FetchContent)

FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        v2.12.0
)

FetchContent_MakeAvailable(pybind11)

pybind11_add_module(strategy_py src/bindings.cpp src/strategy.cpp src/csv_loader.cpp)

# Google Test
enable_testing()
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

# Test executable
add_executable(strategy_test tests/strategy_test.cpp src/strategy.cpp)
target_link_libraries(strategy_test GTest::GTest GTest::Main pthread)

# Register the test
add_test(NAME StrategyTest COMMAND strategy_test)

# For later: target_link_libraries(momentum_strategy TBB::tbb Threads::Threads)
