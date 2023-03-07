# Telegram Movie Bot

MovieBot is a Telegram bot that recommends movies based on data from my personal movie database on Notion. I use it to discover new movies to watch every week.

## Table of contents

- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributions](#contributions)

## Getting Started

To install MovieBot, you'll need to follow these steps:

- Clone the repository to your local machine.
- Install the required dependencies using pip install -r requirements.txt.
- Create a Telegram bot using the BotFather and obtain your bot token.
- Create a Notion API key by following the instructions provided in the official Notion API documentation.
- Set the environment variables TELEGRAM_TOKEN and NOTION_API_KEY to your Telegram bot token and Notion API key, respectively.
- Configure the DATABASE_URL variable in config.py to point to the Notion database that contains your movie data.

## Usage

Once you've set up the bot, you can start it by running python main.py.

The bot will send you a message once a week with a movie recommendation that you haven't seen yet. You can interact with the bot by sending it messages or commands.

The following commands are currently supported:

- /start: Start the bot and receive the first message.
- /recommend: Receive a new movie recommendation.
- /list: Get a list of 10 random movies in your Notion database.
- /help: Get a list of available commands.

## Contributions

As this is a personal pet project, I'm not currently accepting contributions. However, if you have any feedback or suggestions, feel free to open an issue in the repository.
