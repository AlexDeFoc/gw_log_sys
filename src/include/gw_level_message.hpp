#ifndef _GW_LOG_SYSTEM__LEVEL_MESSAGE_HPP_
#define _GW_LOG_SYSTEM__LEVEL_MESSAGE_HPP_

// Library namespace
namespace gw::log {

// Log Level Message
struct LevelMessage {
  static constexpr const char* k_info{"[INFO]"};
  static constexpr const char* k_warning{"[WARNING]"};
  static constexpr const char* k_error{"[ERROR]"};
  static constexpr const char* k_debug{"[DEBUG]"};
};

}  // namespace gw::log

#endif  // _GW_LOG_SYSTEM__LEVEL_MESSAGE_HPP_