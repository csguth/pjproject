cmake_minimum_required(VERSION 3.0.2)

project(callpp VERSION 0.1)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_executable(main main.cpp)

target_link_libraries(main CONAN_PKG::pjproject)
