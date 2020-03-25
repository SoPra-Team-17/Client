cmake_minimum_required(VERSION 3.10)
project(SampleTest)

set(CMAKE_CXX_STANDARD 17)

add_executable(SampleTest main.cpp)

target_link_libraries(SampleTest SampleLibrary)