cmake_minimum_required(VERSION 3.10)
project(SampleLibrary)

set(CMAKE_CXX_STANDARD 17)

add_library(SampleLibrary SHARED library.cpp library.h)

install(TARGETS SampleLibrary DESTINATION /usr/lib)
install(FILES library.h
        DESTINATION /usr/include/SampleLibrary)