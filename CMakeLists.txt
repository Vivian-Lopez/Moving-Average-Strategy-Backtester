cmake_minimum_required(VERSION 3.16)
project(MomentumStrategy)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(include)

add_executable(momentum_strategy
    src/main.cpp
    src/strategy.cpp
)

# For later: target_link_libraries(momentum_strategy TBB::tbb Threads::Threads)
