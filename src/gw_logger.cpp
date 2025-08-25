// Subject being implemented
#include "../include/gw_logger.hpp"

// Helper functions
// clang-format off
namespace {
auto ComposeMessage(gw::log::Level p_level, std::string_view p_text) noexcept -> std::string {
  switch (p_level) {
    case gw::log::Level::k_none:
      return std::format("{}", p_text);
    case gw::log::Level::k_info: {
      return std::format("{}: {}", gw::log::LevelMessage::k_info, p_text);
      break;
    }
    case gw::log::Level::k_warning: {
      return std::format("{}: {}", gw::log::LevelMessage::k_warning, p_text);
      break;
    }
    case gw::log::Level::k_error: {
      return std::format("{}: {}", gw::log::LevelMessage::k_error, p_text);
      break;
    }
    case gw::log::Level::k_debug: {
      return std::format("{}: {}", gw::log::LevelMessage::k_debug, p_text);
      break;
    }
    default:
      return {};
  }
}
}  // namespace
// clang-format on

// Implementation
// Constructors
gw::log::Logger::Logger() noexcept : m_log_level{gw::log::Level::k_info} {}

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