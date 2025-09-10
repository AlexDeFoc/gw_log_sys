#pragma once

// gw_log_sys --- Logging library used by gameWatch
// Copyright 2025 - Sava Alexandru-Andrei
// Licensed under the MIT Licence. See LICENSE.md file in project root.

#include <string_view>
#include <string>
#include <atomic>
#include <mutex>
#include "./gw_log_sys_api.hpp"
#include "./gw_log_levels.hpp"

namespace gw::log {
class Message {
public:
    using TextType = std::string;

private:
    mutable std::mutex m_mutex;
    std::string m_text;
    std::atomic<gw::log::LogLevel> m_log_level;
    std::atomic<bool> m_should_color_log_level_message;

public:
    GW_LOG_SYS_API Message() noexcept;

public:
[[nodiscard]] GW_LOG_SYS_API auto getText() const noexcept -> std::string_view;
[[nodiscard]] GW_LOG_SYS_API auto getLogLevel() const noexcept -> gw::log::LogLevel;
[[nodiscard]] GW_LOG_SYS_API auto getLogLevelMessage() const noexcept -> std::string_view;
[[nodiscard]] GW_LOG_SYS_API auto getShouldColorLogLevelMessage() const noexcept -> bool;

public:
GW_LOG_SYS_API auto setText(std::string_view text) noexcept -> void;
GW_LOG_SYS_API auto setLogLevel(gw::log::LogLevel log_level) noexcept -> void;
GW_LOG_SYS_API auto setShouldColorLogLevelMessage(bool should_color) noexcept -> void;
};
}
