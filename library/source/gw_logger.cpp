#include <format>
#include "../include/gw_logger.hpp"

// Helper enum class
enum class UsingAnsiColorsStatus: std::uint8_t { Enabled, Failed, NotAvailable, Unset };

// OS specific stuff
#if defined (_WIN32)

#include <Windows.h>

// Helper functions
[[nodiscard]] auto shouldUseAnsiColorsInTerminal() -> UsingAnsiColorsStatus
{
    static UsingAnsiColorsStatus status = UsingAnsiColorsStatus::Unset;

    if (status == UsingAnsiColorsStatus::Enabled || status == UsingAnsiColorsStatus::NotAvailable)
        return status;

    HANDLE stdout_handle = GetStdHandle(STD_OUTPUT_HANDLE);
    if (stdout_handle == INVALID_HANDLE_VALUE)
    {
        status = UsingAnsiColorsStatus::Failed;
        return status;
    }

    DWORD current_stdout_mode{};
    BOOL action_status = GetConsoleMode(stdout_handle, &current_stdout_mode);
    if (action_status == 0)
    {
        status = UsingAnsiColorsStatus::Failed;
        return status;
    }

    current_stdout_mode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;

    action_status = SetConsoleMode(stdout_handle, current_stdout_mode);
    if (action_status == 0)
    {
        status = UsingAnsiColorsStatus::Failed;
        return status;
    }

    status = UsingAnsiColorsStatus::Enabled;
    return status;
}
#else

// Helper functions
[[nodiscard]] auto enableANSIColorsInWindowsTerminal() -> UsingAnsiColorsStatus { return UsingAnsiColorsStatus::Enabled; } // todo(alex): check on unix
                                                                                                                           // if actually terminal supports
                                                                                                                           // or has enabled colors
#endif

[[nodiscard]] auto colorLogLevelMessage(std::string_view msg, gw::log::LogLevel log_level) -> std::string
{
    std::string_view ansi_color_prefix{};

    switch(log_level)
    {
        case gw::log::LogLevel::None:
            ansi_color_prefix = "\x1b[37m";
            break;
        case gw::log::LogLevel::Info:
            ansi_color_prefix = "\x1b[36m";
            break;
        case gw::log::LogLevel::Warning:
            ansi_color_prefix = "\x1b[33m";
            break;
        case gw::log::LogLevel::Error:
            ansi_color_prefix = "\x1b[31m";
            break;
        case gw::log::LogLevel::Debug:
            ansi_color_prefix = "\x1b[35m";
            break;
    }

    return std::format("{}{}{}", ansi_color_prefix, msg, "\x1b[0m");
}

// Class methods
gw::log::Logger::Logger() noexcept : m_log_level{gw::log::LogLevel::None}, m_should_color_log_level_msg{true} {}

auto gw::log::Logger::getLogLevel() const noexcept -> gw::log::LogLevel
{
    return this->m_log_level.load(std::memory_order_relaxed);
}

auto gw::log::Logger::setLogLevel(gw::log::LogLevel log_level) noexcept -> void
{
    this->m_log_level.store(log_level, std::memory_order_relaxed);
}

auto gw::log::Logger::shouldColorLogLevelMsg(bool should_it_color) noexcept -> void
{
    this->m_should_color_log_level_msg.store(should_it_color, std::memory_order_relaxed);
}

auto gw::log::Logger::print(const gw::log::Message& msg, std::ostream& output_stream) const noexcept -> void
{
    if (msg.getLogLevel() <= this->m_log_level.load(std::memory_order_relaxed))
    {
        std::lock_guard<std::mutex> lock(this->m_mutex);

        const UsingAnsiColorsStatus useAnsiColorsStatus = shouldUseAnsiColorsInTerminal();

        std::string formatted_message{};

        if (this->m_should_color_log_level_msg.load() && useAnsiColorsStatus == UsingAnsiColorsStatus::Enabled)
        {
            const std::string coloredLogLevelMessage = colorLogLevelMessage(msg.getLogLevelMessage(), msg.getLogLevel());
            formatted_message =  std::format("{}: {}", coloredLogLevelMessage, msg.getText());
        }
        else
            formatted_message =  std::format("{}: {}", msg.getLogLevelMessage(), msg.getText());

        output_stream << formatted_message;
    }
}

auto gw::log::Logger::println(const gw::log::Message& msg, std::ostream& output_stream) const noexcept -> void
{
    if (msg.getLogLevel() <= this->m_log_level.load(std::memory_order_relaxed))
    {
        std::lock_guard<std::mutex> lock(this->m_mutex);

        const UsingAnsiColorsStatus useAnsiColorsStatus = shouldUseAnsiColorsInTerminal();

        std::string formatted_message{};

        if (msg.getShouldColorLogLevelMessage() && this->m_should_color_log_level_msg.load() && useAnsiColorsStatus == UsingAnsiColorsStatus::Enabled)
        {
            const std::string coloredLogLevelMessage = colorLogLevelMessage(msg.getLogLevelMessage(), msg.getLogLevel());
            formatted_message =  std::format("{}: {}\n", coloredLogLevelMessage, msg.getText());
        }
        else
            formatted_message =  std::format("{}: {}\n", msg.getLogLevelMessage(), msg.getText());

        output_stream << formatted_message;
    }
}

auto gw::log::Logger::getHandle() noexcept -> gw::log::Logger::Handle&
{
    static gw::log::Logger::Handle logger_handle{};

    return logger_handle;
}
