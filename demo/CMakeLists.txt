cmake_minimum_required(VERSION 3.20)
project(FactExporter)

find_package(LLVM REQUIRED CONFIG)
find_package(Clang REQUIRED CONFIG)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include_directories(${LLVM_INCLUDE_DIRS})
include_directories(${CLANG_INCLUDE_DIRS})
add_definitions(${LLVM_DEFINITIONS})

add_executable(FactExporter main.cpp FactExporter.cpp)

llvm_map_components_to_libnames(llvm_libs support core irreader option)
target_link_libraries(FactExporter
  PRIVATE
    clangAST
    clangBasic
    clangFrontend
    clangTooling
    clangASTMatchers
    ${llvm_libs}
)
