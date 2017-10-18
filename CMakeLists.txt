cmake_minimum_required (VERSION 3.5)
project (dino)

# Set some compiler flags
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --std=c++14")

# Build vendored libraries
add_subdirectory (${CMAKE_CURRENT_SOURCE_DIR}/lib/caf)

# Include directories
include_directories (${CAF_INCLUDE_DIR})

# Link directories
link_directories (${CAF_LIBRARY_DIR})
message (${CAF_LIBRARY_DIR})

# Convenience variables
set (DINO_DEPS
  ${CAF_EXTERNAL_PROJECT}
  )

set (DINO_LIBRARIES
  caf_core
  caf_io
  )

add_executable (
  ${PROJECT_NAME}
  ${CMAKE_CURRENT_SOURCE_DIR}/cxx/test.cpp
  )

add_dependencies (${PROJECT_NAME} ${DINO_DEPS})
target_link_libraries (${PROJECT_NAME} ${DINO_LIBRARIES})
