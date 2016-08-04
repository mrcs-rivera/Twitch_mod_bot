# cfg.py
HOST = "irc.chat.twitch.tv"                          # Twitch irc host
PORT = 6667                                          # IRC port
NICK = "BOT_USERNAME"                                # your Twitch username, lowercase
PASS = "oauth:TWITCH_OAUTHT_OKEN"                    # your Twitch OAuth token\
CHANNELS = ["CAHNNEL_TO_JOIN"]                       # the channels you want to join
RATE = (20/30)                                       # messages per second, if bot is modded then 1000/30 can be used

PATT = [r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',  # urls
        ]
