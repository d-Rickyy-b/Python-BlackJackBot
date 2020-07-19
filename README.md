[![Build Status](https://travis-ci.com/d-Rickyy-b/Python-BlackJackBot.svg?branch=master)](https://travis-ci.com/d-Rickyy-b/Python-BlackJackBot) [![Code Health](https://landscape.io/github/d-Rickyy-b/Python-BlackJackBot/master/landscape.svg?style=flat)](https://landscape.io/github/d-Rickyy-b/Python-BlackJackBot/master)

# Python-BlackJackBot

This is the code for my Telegram Bot with which you can play the game Black Jack. You can find it here: https://telegram.me/BlackJackBot

The main file, which needs to be executed is 'main.py'.
You need to put your API-Token in the right place in the main file.

## Other Software

The bot uses the [python-telegram-bot](https://python-telegram-bot.org/) framework to make Telegram API calls. You can install it like that:

``pip install python-telegram-bot``

## Database

The bot uses a SQLite database. The database file is in the "database" directory. It is called 'users.db'. The database gets auto-generated, if it doesn't exist. Make sure the program has write access to the database directory.
