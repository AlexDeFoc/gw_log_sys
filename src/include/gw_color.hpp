#ifndef _GW_LOG_SYSTEM__COLOR_HPP_
#define _GW_LOG_SYSTEM__COLOR_HPP_

// Library namespace
namespace gw::log {

// Color structure
struct Color {
  static constexpr const char *k_cyan{"\x1b[36m"};
  static constexpr const char *k_yellow{"\x1b[33m"};
  static constexpr const char *k_red{"\x1b[31m"};
  static constexpr const char *k_magenta{"\x1b[35m"};
  static constexpr const char *k_reset{"\x1b[0m"};
};

}  // namespace gw::log

#endif  // _GW_LOG_SYSTEM__COLOR_HPP_