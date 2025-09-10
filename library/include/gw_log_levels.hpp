#pragma once

// gw_log_sys --- Logging library used by gameWatch
// Copyright 2025 - Sava Alexandru-Andrei
// Licensed under the MIT Licence. See LICENSE.md file in project root.

#include <cstdint>

namespace gw::log {
enum class LogLevel : uint8_t { None = 0,  Info, Warning, Error, Debug};
}
