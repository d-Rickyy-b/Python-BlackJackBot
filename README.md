[![Build Status](https://travis-ci.com/d-Rickyy-b/Python-BlackJackBot.svg?branch=master)](https://travis-ci.com/d-Rickyy-b/Python-BlackJackBot)
[![Coverage Status](https://coveralls.io/repos/github/d-Rickyy-b/Python-BlackJackBot/badge.svg?branch=rebuild)](https://coveralls.io/github/d-Rickyy-b/Python-BlackJackBot?branch=rebuild)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/12996d68fc0f436085221ac6b1f525f9)](https://www.codacy.com/manual/d-Rickyy-b/Python-BlackJackBot?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=d-Rickyy-b/Python-BlackJackBot&amp;utm_campaign=Badge_Grade)

# Python-BlackJackBot

This is the code for my Telegram Bot with which you can play the game Black Jack. You can find it here: https://telegram.me/BlackJackBot

The main file, which needs to be executed is 'main.py'. Please create a copy of the config.sample.py, name it config.py and enter the config data (e.g. bot
 token).

## Setup

The bot uses the [python-telegram-bot](https://python-telegram-bot.org/) framework to make Telegram API calls. You can install it like that:

``pip install -r requirements.txt``

## Database

The bot uses a SQLite database. The database file is in the "database" directory. It is called 'users.db'. The database gets auto-generated, if it doesn't exist. Make sure the program has write access to the database directory.
