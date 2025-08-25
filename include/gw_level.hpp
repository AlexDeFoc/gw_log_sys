#ifndef _GW_LOG_SYSTEM__LEVEL_HPP_
#define _GW_LOG_SYSTEM__LEVEL_HPP_

// Standard C++ libraries
#include <cstdint>

// Library namespace
namespace gw::log {

// Log Level
enum class Level : std::uint8_t { k_none, k_info, k_warning, k_error, k_debug };

// Log Level Message
struct LevelMessage {
  static inline const char* k_info{"[INFO]"};
  static inline const char* k_warning{"[WARNING]"};
  static inline const char* k_error{"[ERROR]"};
  static inline const char* k_debug{"[DEBUG]"};
};

}  // namespace gw::log

#endif  // _GW_LOG_SYSTEM__LEVEL_HPP_