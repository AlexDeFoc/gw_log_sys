#ifndef _GW_LOG_SYSTEM__LOGGER_HPP_
#define _GW_LOG_SYSTEM__LOGGER_HPP_

// Standard C++ libraries
#include <iostream>

// Internal headers
#include "./gw_build_dll.hpp"
#include "./gw_level.hpp"
#include "./gw_message.hpp"

// Library namespace
namespace gw::log {

// Logger class
class Logger {
 public:
  GW_EXPOSE_TO_DLL Logger() noexcept;
  GW_EXPOSE_TO_DLL explicit Logger(gw::log::Level p_level) noexcept;

  [[nodiscard]] GW_EXPOSE_TO_DLL auto GetLogLevel() const noexcept
      -> gw::log::Level;

  GW_EXPOSE_TO_DLL void SetLogLevel(gw::log::Level p_level) noexcept;

  // clang-format off
  GW_EXPOSE_TO_DLL void Log(const gw::log::Message& p_msg,
                            std::ostream& p_output_stream = std::cout) const noexcept;
  // clang-format on

 private:
  gw::log::Level m_log_level;
};

}  // namespace gw::log

#endif  // _GW_LOG_SYSTEM__LOGGER_HPP_