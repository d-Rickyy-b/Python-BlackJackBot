from telegram.ext import BaseFilter


# A filter which returns True, if a message is sent in an allowed group and False if not.
class _ChannelFilter(BaseFilter):
    name = "ChannelFilter"

    def filter(self, message):
        if message.chat.type == "channel":
            return True

        return False


ChannelFilter = _ChannelFilter()
