import bot
import argparse

parser = argparse.ArgumentParser(description="Run Twitch bot.")
parser.add_argument('-d', '--debug', help='Turn on debug output.')
parser.add_argument('-p', '--print',  help='Print Twitch messages')
args = parser.parse_args()
print("hello world")
print(args)

