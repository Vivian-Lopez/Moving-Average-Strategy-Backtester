cmake_minimum_required(VERSION 3.16)
project(MomentumStrategy)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

# === Main Executable ===
add_executable(momentum_strategy
    src/main.cpp
    src/strategy.cpp
    src/csv_loader.cpp
)

# === pybind11 ===
include(FetchContent)

FetchContent_Declare(
  pybind11
  GIT_REPOSITORY https://github.com/pybind/pybind11.git
  GIT_TAG        v2.12.0
)
FetchContent_MakeAvailable(pybind11)

pybind11_add_module(strategy_py src/bindings.cpp src/strategy.cpp src/csv_loader.cpp)

# === Google Test ===
FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG        v1.14.0
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

enable_testing()

# === Test Executable ===
add_executable(strategy_test tests/strategy_test.cpp src/strategy.cpp)

# Link to actual gtest libraries
target_link_libraries(strategy_test gtest gtest_main pthread)

add_test(NAME StrategyTest COMMAND strategy_test)

# === Optional Parallelism (for later) ===
# target_link_libraries(momentum_strategy TBB::tbb Threads::Threads)
