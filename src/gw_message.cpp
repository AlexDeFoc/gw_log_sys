// Subject being implemented
#include "../include/gw_message.hpp"

// Implementation
// Constructors
gw::log::Message::Message() noexcept : m_log_level{gw::log::Level::k_none} {}

// Getters
auto gw::log::Message::GetText() const noexcept -> std::string_view {
  return this->m_text;
}

auto gw::log::Message::GetLogLevel() const noexcept -> gw::log::Level {
  return this->m_log_level;
}

// Setters
void gw::log::Message::SetText(const char *p_text) noexcept {
  this->m_text = p_text;
}

void gw::log::Message::SetLogLevel(gw::log::Level p_level) noexcept {
  this->m_log_level = p_level;
}