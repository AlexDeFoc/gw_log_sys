// External libraries
#include <gtest/gtest.h>

// Internal libraries
#include "../../../include/gw_message.hpp"

// Tests
TEST(Message, ConfirmingDefaultInitialization) {
  gw::log::Message msg{};

  EXPECT_EQ(msg.GetLogLevel(), gw::log::Level::k_none);
}

TEST(Message, ConfiguringMessage) {
  gw::log::Message msg{};

  msg.SetLogLevel(gw::log::Level::k_info);
  msg.SetText("Testing message");

  EXPECT_TRUE(msg.GetText() == "Testing message");
  EXPECT_EQ(msg.GetLogLevel(), gw::log::Level::k_info);
}

TEST(Message, SetTextUsingRawString) {
  gw::log::Message msg{};

  msg.SetText("Testing message");

  EXPECT_TRUE(msg.GetText() == "Testing message");
}

TEST(Message, SetTextUsingStandardString) {
  gw::log::Message msg{};

  const std::string k_text{"Testing message"};
  msg.SetText(k_text);

  EXPECT_TRUE(msg.GetText() == "Testing message");
}