#pragma once

// gw_log_sys --- Logging library used by gameWatch
// Copyright 2025 - Sava Alexandru-Andrei
// Licensed under the MIT Licence. See LICENSE.md file in project root.

#include <atomic>
#include <iostream>
#include <mutex>
#include "./gw_message.hpp"

namespace gw::log {
struct LoggerConfig
{
    gw::log::LogLevel log_level;
    bool should_color_log_level_message;
};

class Logger
{
public:
    using Handle = Logger;
private:
    mutable std::mutex m_mutex;
    std::atomic<gw::log::LogLevel> m_log_level;
    std::atomic<bool> m_should_color_log_level_message;

public:
    GW_LOG_SYS_API Logger() noexcept;
    GW_LOG_SYS_API ~Logger() noexcept = default;
    Logger(const Logger& other) noexcept = delete;
    Logger(Logger&& other) noexcept = delete;
    Logger& operator=(const Logger& other) noexcept = delete;
    Logger& operator=(Logger&& other) noexcept = delete;

public:
    [[nodiscard]] GW_LOG_SYS_API auto getLogLevel() const noexcept -> gw::log::LogLevel;
    [[nodiscard]] GW_LOG_SYS_API static auto getHandle() noexcept -> Handle&;
    [[nodiscard]] GW_LOG_SYS_API auto getShouldColorLogLevelMessageStatus() const noexcept -> bool;

public:
    GW_LOG_SYS_API auto setLogLevel(gw::log::LogLevel log_level) noexcept -> void;
    GW_LOG_SYS_API auto setShouldColorLogLevelMsg(bool should_it_color) noexcept -> void;

public:
    GW_LOG_SYS_API auto println(const gw::log::Message& msg, std::ostream& output_stream = std::cout) const noexcept -> void;
    GW_LOG_SYS_API auto print(const gw::log::Message& msg, std::ostream& output_stream = std::cout) const noexcept -> void;
    GW_LOG_SYS_API auto configure(const LoggerConfig& logger_config) noexcept -> void;
};
}
