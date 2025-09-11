#include "../include/gw_message.hpp"

gw::log::Message::Message() noexcept : m_text{"Invalid text"}, m_log_level{gw::log::LogLevel::None}, m_should_color_log_level_message{true} {};

auto gw::log::Message::getText() const noexcept -> std::string_view
{
    std::lock_guard<std::mutex> lock(this->m_mutex);
    return std::string_view{this->m_text};
}

auto gw::log::Message::getLogLevel() const noexcept -> gw::log::LogLevel
{
    return this->m_log_level.load(std::memory_order_relaxed);
}

auto gw::log::Message::getLogLevelMessage() const noexcept -> std::string_view
{
    std::string_view log_level_msg{};

    switch(this->m_log_level.load(std::memory_order_relaxed))
    {
        case gw::log::LogLevel::None:
            log_level_msg = "";
            break;
        case gw::log::LogLevel::Info:
            log_level_msg = "[INFO]";
            break;
        case gw::log::LogLevel::Warning:
            log_level_msg = "[WARNING]";
            break;
        case gw::log::LogLevel::Error:
            log_level_msg = "[ERROR]";
            break;
        case gw::log::LogLevel::Debug:
            log_level_msg = "[DEBUG]";
            break;
    }

    return log_level_msg;
}

auto gw::log::Message::getShouldColorLogLevelMessage() const noexcept -> bool
{
    return this->m_should_color_log_level_message.load(std::memory_order_relaxed);
}

auto gw::log::Message::setText(std::string_view text) noexcept -> void
{
    std::lock_guard<std::mutex> lock(this->m_mutex);
    this->m_text = text;
}

auto gw::log::Message::setLogLevel(gw::log::LogLevel log_level) noexcept -> void
{
    this->m_log_level.store(log_level, std::memory_order_relaxed);
}

auto gw::log::Message::setShouldColorLogLevelMessage(bool should_color) noexcept -> void
{
    this->m_should_color_log_level_message.store(should_color, std::memory_order_relaxed);
}

auto gw::log::Message::configure(const gw::log::MessageConfig& msg_cfg) noexcept -> void
{
    std::lock_guard<std::mutex> lock(this->m_mutex);
    this->m_text = msg_cfg.text;
    this->m_log_level.store(msg_cfg.log_level, std::memory_order_relaxed);
    this->m_should_color_log_level_message.store(msg_cfg.should_color_log_level_message, std::memory_order_relaxed);
}
