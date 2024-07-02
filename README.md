# Discord Bot for Web Scraping and Monitoring

**Clappy** is a versatile Discord bot that empowers you to monitor multiple online stores by scraping product data and sending updates directly to your Discord server. This bot is designed to be user-friendly, making web scraping accessible to everyone.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Commands](#commands)
- [Hosting](#hosting)
- [Proxies](#proxies)
- [Screenshots](#screenshots)

## Features

- Monitor Backmarket and GSMWarehouse for product changes.
- Real-time updates: Receive notifications when product data is updated.
- User-friendly Discord commands for managing the bot.
- CSV export: Store product data in a convenient CSV format.
- Easy deployment using online hosting services like Heroku.

## Installation

1. Clone this repository or download the ZIP file.
2. Ensure you have Python 3.x installed.
3. Install the required packages by running:

pip install -r requirements.txt

4. Set up your Discord bot token in `discord_bot.py`.
5. If using proxies, provide them in `http_proxies.txt` and run `proxy_generator.py`.
6. Run the bot with the following command:

## Usage

1. Invite your bot to your Discord server.
2. Customize your server's configuration.
3. Use Clappy's commands to manage and monitor the bot.
4. Sit back and let Clappy handle the monitoring for you.

## Commands

- `!welcoming`: Get a friendly welcome message from Clappy.
- `!custom_help`: View available commands and their descriptions.
- `!Backmarket`: Check if Backmarket monitoring is operational.
- `!GSMWarehouse`: Check if GSMWarehouse monitoring is operational.
- `!add_url [store] [url]`: Add a product URL for monitoring.
- `!remove_url [store] [url]`: Remove a product URL from monitoring.
- `!backmarket_database`: Export Backmarket product data in CSV format.
- `!gsm_database`: Export GSMWarehouse product data in CSV format.
- `!start_scraping [store]`: Start product scraping for a specific store.
- `!stop_scraping [store]`: Stop product scraping for a specific store.

## Hosting

If you prefer not to run the bot on your local machine, you can utilize online hosting services like Heroku. Here's how to do it:

1. Create an account on Heroku.
2. Create a new Heroku app.
3. Set up the Heroku app using the provided documentation.
4. Deploy your project to Heroku using the Heroku CLI or connect your GitHub repository.

## Proxies

If you need to use proxies, you can provide them in `http_proxies.txt` and run `proxy_generator.py` on your computer. Then, upload the resulting file to the server.


---

**Disclaimer:** This project is for educational purposes and adheres to all terms and conditions of the websites being monitored. It should not be used for any unauthorized or unethical activities.
