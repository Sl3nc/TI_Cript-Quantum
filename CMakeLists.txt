cmake_minimum_required(VERSION 3.16)
project(ti_cript_quantum C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "" FORCE)
endif()

add_compile_options(-Wall -Wextra -Wpedantic)

find_package(OpenSSL 3.0 REQUIRED COMPONENTS Crypto)

find_package(liboqs QUIET)
if(NOT liboqs_FOUND)
    find_package(PkgConfig REQUIRED)
    pkg_check_modules(LIBOQS REQUIRED IMPORTED_TARGET liboqs)
    add_library(OQS::oqs ALIAS PkgConfig::LIBOQS)
endif()

add_library(workloads STATIC
    src/config.c
    src/algorithms/kem.c
    src/algorithms/dss.c
    src/algorithms/mceliece.c
    src/algorithms/ecies.c
    src/algorithms/ecdsa.c
    src/algorithms/ecdh.c
)
target_include_directories(workloads PUBLIC src)
target_link_libraries(workloads PUBLIC OQS::oqs OpenSSL::Crypto)

add_executable(benchmark src/index.c)
target_link_libraries(benchmark PRIVATE workloads)

enable_testing()
add_subdirectory(tests)
