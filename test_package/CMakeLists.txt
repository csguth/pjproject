cmake_minimum_required(VERSION 3.0.2)

project(callpp VERSION 0.1)

macro(ADD_OSX_FRAMEWORK fwname target)
    find_library(FRAMEWORK_${fwname}
    NAMES ${fwname}
    PATHS ${CMAKE_OSX_SYSROOT}/System/Library
    PATH_SUFFIXES Frameworks
    NO_DEFAULT_PATH)
    if( ${FRAMEWORK_${fwname}} STREQUAL FRAMEWORK_${fwname}-NOTFOUND)
        MESSAGE(ERROR ": Framework ${fwname} not found")
    else()
        TARGET_LINK_LIBRARIES(${target} "${FRAMEWORK_${fwname}}")
        MESSAGE(STATUS "Framework ${fwname} found at ${FRAMEWORK_${fwname}}")
    endif()
endmacro(ADD_OSX_FRAMEWORK)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_executable(main main.cpp)
target_compile_definitions(main PUBLIC -DARM)
target_compile_definitions(main PUBLIC -DPJ_IS_LITTLE_ENDIAN=1)
target_compile_definitions(main PUBLIC -DPJ_IS_BIG_ENDIAN=0)

target_link_libraries(main CONAN_PKG::pjproject)

ADD_OSX_FRAMEWORK(CoreAudio main)
ADD_OSX_FRAMEWORK(AudioUnit main)
ADD_OSX_FRAMEWORK(AudioToolbox main)
ADD_OSX_FRAMEWORK(CoreFoundation main)
  
     