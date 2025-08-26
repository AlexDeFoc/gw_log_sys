#pragma once

// Standard C++ libraries
#include <cstdint>

// Library namespace
namespace gw::log {

// Log Level enum class
enum class Level : std::uint8_t { k_none, k_info, k_warning, k_error, k_debug };

}  // namespace gw::log