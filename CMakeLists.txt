# CMake setup
cmake_minimum_required(VERSION 4.1.0)
project(gw_log_system CXX)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# C++ setup
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Options
option(BUILD_TESTS "Build tests" OFF)
option(BUILD_STATIC_LIBRARY "Build statically linked library instead of dynamically linked" OFF)

# Compiler flags
if (MSVC)
	set(error_flags /W4 /WX)
else()
	set(error_flags -Wall -Wextra -Werror)
endif()

# Library source files
set(lib_src
	src/gw_message.cpp
	src/gw_logger.cpp
)

# Library header directories
set(public_lib_includes
	include
)

set(private_lib_includes
	src/include
)

# Library setup
if (BUILD_STATIC_LIBRARY)
	add_library(gw_log_system STATIC ${lib_src})
	target_compile_definitions(gw_log_system PUBLIC DontBuildDll)
else()
	add_library(gw_log_system SHARED ${lib_src})
	if (CMAKE_SYSTEM_NAME STREQUAL "Windows")
		target_compile_definitions(gw_log_system PRIVATE BuildDll)
	endif()
endif()

target_compile_options(gw_log_system PRIVATE ${error_flags})
target_include_directories(gw_log_system
	PUBLIC ${public_lib_includes}
	PRIVATE ${private_lib_includes}
)

# Tests category
if (BUILD_TESTS)
	# Tests source files
	set(test_src
		test/general_testing/src/test_gw_message.cpp
		test/general_testing/src/test_gw_logger.cpp
	)

	# Dependencies
	# GoogleTest
	include(FetchContent)
	if (MSVC)
		# For Windows: Prevent overriding the parent project's compiler/linker settings
		set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
	endif()
	FetchContent_Declare(
		googletest
		URL https://github.com/google/googletest/archive/52eb8108c5bdec04579160ae17225d66034bd723.zip
	)
	FetchContent_MakeAvailable(googletest)

	# Tests setup
	add_executable(gw_log_system_tests ${test_src})
	target_compile_options(gw_log_system_tests PRIVATE ${error_flags})
	target_link_libraries(gw_log_system_tests PRIVATE gw_log_system GTest::gtest_main)
	target_include_directories(gw_log_system_tests PUBLIC ${test_includes})

	include(GoogleTest)
	gtest_discover_tests(gw_log_system_tests)
endif()