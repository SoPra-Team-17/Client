cmake_minimum_required(VERSION 3.10)
project(SampleLibrary)

set(CMAKE_CXX_STANDARD 17)

add_library(SampleLibrary SHARED Model.cpp CallbackClass.cpp Network.cpp)

install(TARGETS SampleLibrary DESTINATION /usr/lib)
install(FILES Model.hpp CallbackClass.hpp Network.hpp
        DESTINATION /usr/include/SampleLibrary)