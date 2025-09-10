cmake_minimum_required(VERSION 4.1.1)
project(gw_log_sys LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

option(BUILD_STATIC_LIB__GW_LOG_SYS "Build static library" TRUE)
option(BUILD_TESTS__GW_LOG_SYS "Build tests" TRUE)

if (MSVC)
    set(COMPILER_FLAGS__GW_LOG_SYS /W4 /WX /permissive-)
else()
    set(COMPILER_FLAGS__GW_LOG_SYS -Wall -Wpedantic -Wextra -Werror -Wconversion -Wshadow)
endif()

set(LIB_CPP_FILES__GW_LOG_SYS
    library/source/gw_message.cpp
    library/source/gw_logger.cpp)

if (BUILD_STATIC_LIB__GW_LOG_SYS)
    add_library(gw_log_sys STATIC ${LIB_CPP_FILES__GW_LOG_SYS})
    target_compile_definitions(gw_log_sys PUBLIC DONT_BUILD_DLL__GW_LOG_SYS)
else()
    add_library(gw_log_sys SHARED ${LIB_CPP_FILES__GW_LOG_SYS})
    target_compile_definitions(gw_log_sys PUBLIC BUILD_DLL__GW_LOG_SYS)
endif()

target_compile_options(gw_log_sys PRIVATE ${COMPILER_FLAGS__GW_LOG_SYS})
target_include_directories(gw_log_sys PUBLIC library/include)

if (BUILD_TESTS__GW_LOG_SYS)
    set(TESTS_CPP_FILES__GW_LOG_SYS
        tests/source/gw_test_message.cpp
        tests/source/gw_test_logger.cpp)

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

    # Disable GoogleTest warnings
    if (MSVC)
    elseif (CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
        target_compile_options(gtest PRIVATE -Wno-character-conversion)
        target_compile_options(gtest_main PRIVATE -Wno-character-conversion)
    endif()

	# Tests setup
    add_executable(gw_log_sys_tests ${TESTS_CPP_FILES__GW_LOG_SYS})
	target_link_libraries(gw_log_sys_tests PRIVATE gw_log_sys GTest::gtest_main)
    target_compile_options(gw_log_sys_tests PRIVATE ${COMPILER_FLAGS__GW_LOG_SYS})
    target_include_directories(gw_log_sys_tests PRIVATE tests/include)

	include(GoogleTest)
	gtest_discover_tests(gw_log_sys_tests)
endif()
