// External libraries
#include <gtest/gtest.h>

// Standard C++ libraries
#include <sstream>

// Internal libraries
#include "../../../include/gw_logger.hpp"

// Tests
TEST(Logger, ConfirmingDefaultInitialization) {
  gw::log::Logger logger{};

  EXPECT_EQ(logger.GetLogLevel(), gw::log::Level::k_info);
}

TEST(Logger, ConfigureLogger) {
  gw::log::Logger logger{};

  logger.SetLogLevel(gw::log::Level::k_warning);

  EXPECT_EQ(logger.GetLogLevel(), gw::log::Level::k_warning);
}

TEST(Logger, LogMessages) {
  gw::log::Message plain_msg{};
  plain_msg.SetText("Plain message");
  plain_msg.SetLogLevel(gw::log::Level::k_none);

  gw::log::Message info_msg{};
  info_msg.SetText("Info message");
  info_msg.SetLogLevel(gw::log::Level::k_info);

  gw::log::Message warning_msg{};
  warning_msg.SetText("Warning message");
  warning_msg.SetLogLevel(gw::log::Level::k_warning);

  gw::log::Message error_msg{};
  error_msg.SetText("Error message");
  error_msg.SetLogLevel(gw::log::Level::k_error);

  // This following message shouldn't be displayed.
  // Reason is that the logger log level is lower then needed for the debug
  // message to be displayed.
  gw::log::Message debug_msg{};
  debug_msg.SetText("Debug message");
  debug_msg.SetLogLevel(gw::log::Level::k_debug);

  gw::log::Logger logger{};
  logger.SetLogLevel(gw::log::Level::k_error);

  std::ostringstream testing_output_stream{};

  logger.Log(plain_msg, testing_output_stream);
  logger.Log(info_msg, testing_output_stream);
  logger.Log(warning_msg, testing_output_stream);
  logger.Log(error_msg, testing_output_stream);
  logger.Log(debug_msg, testing_output_stream);

  std::ostringstream expected_output_stream{};

  // clang-format off
  expected_output_stream << "Plain message" << '\n'
                         << gw::log::LevelMessage::k_info << ": " << "Info message" << '\n'
                         << gw::log::LevelMessage::k_warning << ": " << "Warning message" << '\n'
                         << gw::log::LevelMessage::k_error << ": " << "Error message" << '\n';
  // clang-format on

  EXPECT_EQ(expected_output_stream.str(), testing_output_stream.str());
}