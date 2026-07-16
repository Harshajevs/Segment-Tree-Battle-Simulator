cmake_minimum_required(VERSION 3.15)
project(SegmentTreeGame)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Copy input data if present (generate with scripts/generate_data.py)
if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/data)
    file(COPY data/ DESTINATION ${CMAKE_BINARY_DIR}/data)
else()
    message(WARNING "data/ not found — run scripts/generate_data.py before executing the game")
endif()

add_executable(SegmentTreeGame
    src/SegmentTree.cpp
    src/TreeOperations/BuildOperations.cpp
    src/TreeOperations/QueryOperations.cpp
    src/TreeOperations/UpdateOperations.cpp
    app/main.cpp
)

target_include_directories(SegmentTreeGame PRIVATE include)
