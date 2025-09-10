#include "../include/gw_test_message.hpp"

TEST(Message, NewMessageHoldsDefaultTextAndLogLevel)
{
    gw::log::Message msg{};

    EXPECT_EQ(msg.getText(), "Invalid text");
    EXPECT_EQ(msg.getLogLevel(), gw::log::LogLevel::None);
}

TEST(Message, ChangingText)
{
    gw::log::Message msg{};

    msg.setText("New message text");

    EXPECT_EQ(msg.getText(), "New message text");
}

TEST(Message, ChangingLogLevel)
{
    gw::log::Message msg{};

    msg.setLogLevel(gw::log::LogLevel::Error);

    EXPECT_EQ(msg.getLogLevel(), gw::log::LogLevel::Error);
}

TEST(Message, GetLogLevelMessageBasedOnHeldLogLevel)
{
    gw::log::Message msg{};

    msg.setLogLevel(gw::log::LogLevel::Error);

    EXPECT_EQ(msg.getLogLevelMessage(), "[ERROR]");
}

TEST(Message, ChangingShouldColorLogLevelMsgStatus)
{
    gw::log::Message msg{};

    msg.setShouldColorLogLevelMessage(false);

    EXPECT_EQ(msg.getShouldColorLogLevelMessage(), false);
}
