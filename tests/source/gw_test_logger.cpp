#include "../include/gw_test_logger.hpp"

// OS dependent stuff
#if defined(_WIN32)

// Helper functions
[[nodiscard]] auto isColoredPrintingEnabledInTerminal() -> bool
{
    HANDLE stdout_handle = GetStdHandle(STD_OUTPUT_HANDLE);
    if (stdout_handle == INVALID_HANDLE_VALUE)
        return false;

    DWORD mode{};
    BOOL action_status = GetConsoleMode(stdout_handle, &mode);
    if (action_status == 0)
        return false;

    if ((mode & ENABLE_VIRTUAL_TERMINAL_PROCESSING) != 0)
        return true;

     return false;
}
#else

#include <unistd.h>
#include <cstdlib>

// Helper functions
[[nodiscard]] auto isColoredPrintingEnabledInTerminal() -> bool
{

    bool is_output_stream_a_terminal = static_cast<bool>(isatty(STDOUT_FILENO));
    if (!is_output_stream_a_terminal)
    {
        return false;
    }

    const char* term_env_var = std::getenv("TERM");
    const char* colors_disabled_env_var_variant_1 = std::getenv("NO_COLOR");
    const char* colors_disabled_env_var_variant_2 = std::getenv("CLICOLOR");

    if (term_env_var == nullptr)
    {
        return false;
    }

    std::string term_env_var_string{term_env_var};

    if (!term_env_var_string.contains("color") || colors_disabled_env_var_variant_1 != nullptr)
    {
        return false;
    }

    if (colors_disabled_env_var_variant_2 != nullptr)
    {
        std::string colors_disabled_env_var_variant_2_string{colors_disabled_env_var_variant_2};

        if (colors_disabled_env_var_variant_2_string == "0")
        {
            return false;
        }
    }

    return true;
}
#endif

// Tests
TEST(LocalLogger, NewLoggerHoldsDefaultLogLevel)
{
    gw::log::Logger logger{};

    EXPECT_EQ(logger.getLogLevel(), gw::log::LogLevel::None);
}

TEST(LocalLogger, ChangingLoggerLogLevel)
{
    gw::log::Logger logger{};

    logger.setLogLevel(gw::log::LogLevel::Error);

    EXPECT_EQ(logger.getLogLevel(), gw::log::LogLevel::Error);
}

TEST(LocalLogger, PrintingMessageWithoutNewLineWithColorIfPossible)
{
    gw::log::Message msg{};

    msg.setText("New message text");
    msg.setLogLevel(gw::log::LogLevel::Info);

    gw::log::Logger logger{};

    logger.setLogLevel(gw::log::LogLevel::Error);

    std::ostringstream testing_sink{};

    logger.print(msg, testing_sink);

    std::ostringstream expected_testing_sink{};

    std::string formatted_expected_output{};
    if (isColoredPrintingEnabledInTerminal())
        formatted_expected_output = std::format("\x1b[36m{}\x1b[0m: {}",
                                                msg.getLogLevelMessage(),
                                                msg.getText());
    else
        formatted_expected_output = std::format("{}: {}",
                                                msg.getLogLevelMessage(),
                                                msg.getText());

    expected_testing_sink << formatted_expected_output;

    EXPECT_EQ(testing_sink.str(), expected_testing_sink.str());
}

TEST(LocalLogger, PrintingMessageWithNewLineWithoutColor)
{
    gw::log::Message msg{};

    msg.setText("New message text");
    msg.setLogLevel(gw::log::LogLevel::Info);

    gw::log::Logger logger{};
    logger.setShouldColorLogLevelMsg(false);

    logger.setLogLevel(gw::log::LogLevel::Error);

    std::ostringstream testing_sink{};

    logger.println(msg, testing_sink);

    std::ostringstream expected_testing_sink{};

    std::string formatted_expected_output = std::format("{}: {}\n",
                                                        msg.getLogLevelMessage(),
                                                        msg.getText());

    expected_testing_sink << formatted_expected_output;

    EXPECT_EQ(testing_sink.str(), expected_testing_sink.str());
}

TEST(LocalLogger, PrintMessageWithNewLineButMessageDisallowingItToBeColored)
{
    gw::log::Message msg{};

    msg.setText("New message text");
    msg.setLogLevel(gw::log::LogLevel::Info);
    msg.setShouldColorLogLevelMessage(false);

    gw::log::Logger logger{};

    logger.setLogLevel(gw::log::LogLevel::Error);

    std::ostringstream testing_sink{};

    logger.println(msg, testing_sink);

    std::ostringstream expected_testing_sink{};

    std::string formatted_expected_output = std::format("{}: {}\n",
                                                        msg.getLogLevelMessage(),
                                                        msg.getText());

    expected_testing_sink << formatted_expected_output;

    EXPECT_EQ(testing_sink.str(), expected_testing_sink.str());
}

TEST(LocalLogger, PrintingMessageWithLogLevelLowerThenMaxOfLogger)
{
    gw::log::Message msg{};

    msg.setLogLevel(gw::log::LogLevel::Info);

    gw::log::Logger logger{};

    std::ostringstream testing_sink{};

    logger.print(msg, testing_sink);

    std::ostringstream expected_testing_sink{};

    EXPECT_EQ(testing_sink.str(), expected_testing_sink.str());
}

TEST(LocalLogger, ConfigureLoggerInOneGo)
{
    gw::log::Logger logger{};

    logger.configure({.log_level = gw::log::LogLevel::Error,
                      .should_color_log_level_message = true});

    EXPECT_EQ(logger.getLogLevel(), gw::log::LogLevel::Error);
    EXPECT_EQ(logger.getShouldColorLogLevelMessageStatus(), true);
}

TEST(SingletonLogger, NewLoggerHoldsDefaultLogLevel)
{
    gw::log::Logger::Handle& logger_handle = gw::log::Logger::getHandle();
    logger_handle.setLogLevel(gw::log::LogLevel::None); // reset log level to default, since the previous tests could've changed its value

    EXPECT_EQ(logger_handle.getLogLevel(), gw::log::LogLevel::None);
}

TEST(SingletonLogger, ChangingLoggerLogLevel)
{
    gw::log::Logger::Handle& logger_handle = gw::log::Logger::getHandle();

    logger_handle.setLogLevel(gw::log::LogLevel::Error);

    EXPECT_EQ(logger_handle.getLogLevel(), gw::log::LogLevel::Error);
}

TEST(SingletonLogger, ChangedLoggerLogLevelInPrevTestHoldsSameValueInThisTest)
{
    // should hold same log level, changed in test name: TEST(SingletonLogger, ChangedLoggerLogLevelInPrevTestHoldsSameValueInThisTest)

    gw::log::Logger::Handle& logger_handle = gw::log::Logger::getHandle();

    EXPECT_EQ(logger_handle.getLogLevel(), gw::log::LogLevel::Error);
}
