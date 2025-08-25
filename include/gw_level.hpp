#ifndef _GW_LOG_SYSTEM__LEVEL_HPP_
#define _GW_LOG_SYSTEM__LEVEL_HPP_

// Standard C++ libraries
#include <cstdint>

// Library namespace
namespace gw::log {

// Log Level enum class
enum class Level : std::uint8_t { k_none, k_info, k_warning, k_error, k_debug };

}  // namespace gw::log

#endif  // _GW_LOG_SYSTEM__LEVEL_HPP_