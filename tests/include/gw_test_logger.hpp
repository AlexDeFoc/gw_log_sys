#pragma once

// gw_log_sys --- Logging library used by gameWatch
// Copyright 2025 - Sava Alexandru-Andrei
// Licensed under the MIT Licence. See LICENSE.md file in project root.

#include <gtest/gtest.h>
#include <sstream>
#include <format>
#include "../../library/include/gw_logger.hpp"

#if defined(_WIN32)
#include <Windows.h>
#endif
