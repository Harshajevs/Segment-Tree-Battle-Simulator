cmake_minimum_required(VERSION 3.15)
project(SegmentTreeGame)

set(CMAKE_CXX_STANDARD 17)

# Copy data files to build directory
file(COPY data/ DESTINATION ${CMAKE_BINARY_DIR}/data)

add_executable(SegmentTreeGame
    src/SegmentTree.cpp         # Contains only constructor/update/lcm
    src/TreeOperations/BuildOperations.cpp
    src/TreeOperations/QueryOperations.cpp
    src/TreeOperations/UpdateOperations.cpp
    app/main.cpp
)

target_include_directories(SegmentTreeGame PRIVATE include)
