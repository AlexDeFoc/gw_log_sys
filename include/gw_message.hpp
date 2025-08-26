#pragma once

// Standard C++ libraries
#include <string>
#include <string_view>

// Internal headers
#include "./gw_build_dll.hpp"
#include "./gw_level.hpp"

// Library namespace
namespace gw::log {

// Message class
class Message {
 public:
  GW_EXPOSE_TO_DLL Message() noexcept;

  GW_EXPOSE_TO_DLL void SetText(const char* p_text) noexcept;
  GW_EXPOSE_TO_DLL void SetText(const std::string& p_text) noexcept;
  GW_EXPOSE_TO_DLL void SetLogLevel(gw::log::Level p_level) noexcept;

  [[nodiscard]] GW_EXPOSE_TO_DLL auto GetText() const noexcept
      -> std::string_view;
  [[nodiscard]] GW_EXPOSE_TO_DLL auto GetLogLevel() const noexcept
      -> gw::log::Level;

 private:
  gw::log::Level m_log_level;
  std::string m_text;

 public:
  friend class Message_ConfirmingDefaultInitialization_Test;
  friend class Message_ConfiguringMessage_Test;
};

}  // namespace gw::log