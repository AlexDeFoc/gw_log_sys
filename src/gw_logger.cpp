// Subject being implemented
#include "../include/gw_logger.hpp"

// Standard C++ libraries
#include <format>

// OS dependent code
// Windows code
#ifdef _WIN32

// System Libraries
#include <windows.h>

// Function
namespace {
auto ConfigureConsoleForColor() noexcept -> bool {
  static bool console_configured = false;

  if (console_configured) {
    return true;
  }

  console_configured = true;

  HANDLE std_out = GetStdHandle(STD_OUTPUT_HANDLE);
  if (std_out == INVALID_HANDLE_VALUE) {
    return false;
  }

  DWORD console_mode = 0;
  if (GetConsoleMode(std_out, &console_mode) == 0) {
    return false;
  }

  console_mode |=
      ENABLE_VIRTUAL_TERMINAL_PROCESSING | DISABLE_NEWLINE_AUTO_RETURN;

  if (SetConsoleMode(std_out, console_mode) == 0) {
    return false;
  }

  return console_configured;
}
}  // namespace

// Other OSes
#else
namespace {
auto ConfigureConsoleForColor() noexcept -> bool { return true; }
}  // namespace
#endif

// Internal libraries
#include "./include/gw_color.hpp"
#include "./include/gw_level_message.hpp"

// Helper functions
// clang-format off
namespace {
auto ColorizeLogLevelTag(gw::log::Level p_level) noexcept -> std::string {
  bool console_supports_color = ConfigureConsoleForColor();
  
  switch(p_level) {
    case gw::log::Level::k_none: {
      return {};
    }
    case gw::log::Level::k_info: {
      if (console_supports_color) {
        return std::format("{}{}{}", gw::log::Color::k_cyan, gw::log::LevelMessage::k_info, gw::log::Color::k_reset);
      }  

      return {gw::log::LevelMessage::k_info};
    }
    case gw::log::Level::k_warning: {
      if (console_supports_color) {
        return std::format("{}{}{}", gw::log::Color::k_yellow, gw::log::LevelMessage::k_warning, gw::log::Color::k_reset);
      }  

      return {gw::log::LevelMessage::k_warning};
    }
    case gw::log::Level::k_error: {
      if (console_supports_color) {
        return std::format("{}{}{}", gw::log::Color::k_red, gw::log::LevelMessage::k_error, gw::log::Color::k_reset);
      }  

      return {gw::log::LevelMessage::k_error};
    }
    case gw::log::Level::k_debug: {
      if (console_supports_color) {
        return std::format("{}{}{}", gw::log::Color::k_magenta, gw::log::LevelMessage::k_debug, gw::log::Color::k_reset);
      }  

      return {gw::log::LevelMessage::k_debug};
    }
    default: {
      return {};
    }
  }
}

auto ComposeMessage(gw::log::Level p_level, std::string_view p_text) noexcept -> std::string {
  const std::string k_log_level_tag = ColorizeLogLevelTag(p_level);

  if (p_level == gw::log::Level::k_none) {
    return std::string{p_text};
  }

  return std::format("{}: {}", k_log_level_tag, p_text);
}

}  // namespace
// clang-format on

// Implementation
// Constructors
gw::log::Logger::Logger() noexcept : m_log_level{gw::log::Level::k_none} {}

gw::log::Logger::Logger(gw::log::Level p_level) noexcept
    : m_log_level{p_level} {}

// Getters
auto gw::log::Logger::GetLogLevel() const noexcept -> gw::log::Level {
  return this->m_log_level;
}

// Setters
void gw::log::Logger::SetLogLevel(gw::log::Level p_level) noexcept {
  this->m_log_level = p_level;
}

// General Methods
// clang-format off
void gw::log::Logger::Log(const gw::log::Message& p_msg, std::ostream& p_output_stream) const noexcept {
  if (this->m_log_level >= p_msg.GetLogLevel()) {
    p_output_stream << ComposeMessage(p_msg.GetLogLevel(), p_msg.GetText()) << '\n';
  }
}
// clang-format on