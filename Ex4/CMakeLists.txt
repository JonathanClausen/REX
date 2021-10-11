CMAKE_MINIMUM_REQUIRED (VERSION 2.8.9)
PROJECT(exercise4 CXX)


#FIND_PACKAGE(OpenCV REQUIRED core highgui imgcodecs)
FIND_PACKAGE(OpenCV REQUIRED)

INCLUDE_DIRECTORIES(
		${OpenCV_INCLUDE_DIRS}
		${PROJECT_SOURCE_DIR}/src/handout/C++/
	)

MESSAGE( STATUS "OpenCV_VERSION = ${OpenCV_VERSION}")
MESSAGE( STATUS "OpenCV_LIBS = ${OpenCV_LIBS}")
MESSAGE( STATUS "OpenCV_INCLUDE_DIRS = ${OpenCV_INCLUDE_DIRS}")

SET(SRCS
  ${PROJECT_SOURCE_DIR}/src/handout/C++/camera.cc
  ${PROJECT_SOURCE_DIR}/src/handout/C++/particles.cc
  ${PROJECT_SOURCE_DIR}/src/handout/C++/random_numbers.cc
)

SET(HEADERS
  ${PROJECT_SOURCE_DIR}/src/handout/C++/camera.h
  ${PROJECT_SOURCE_DIR}/src/handout/C++/particles.h
  ${PROJECT_SOURCE_DIR}/src/handout/C++/random_numbers.h
)

SET(DUMMY_MAIN
  ${PROJECT_SOURCE_DIR}/src/handout/C++/exercise4.cc
)

add_executable(exercise5 ${DUMMY_MAIN} ${SRCS} ${HEADERS})
target_link_libraries(exercise5 ${OpenCV_LIBS})

SET(SOLUTION_MAIN
  ${PROJECT_SOURCE_DIR}/src/solutions/solution.cc
)

IF (EXISTS ${SOLUTION_MAIN})
	add_executable(solution ${SOLUTION_MAIN} ${SRCS} ${HEADERS})
	target_link_libraries(solution ${OpenCV_LIBS})
	SET_PROPERTY(TARGET solution APPEND PROPERTY INCLUDE_DIRECTORIES "${PROJECT_SOURCE_DIR}")

	# Only works with CMake 3.3 and onwards
	#target_include_directories(solution PUBLIC ${PROJECT_SOURCE_DIR})
ENDIF()

