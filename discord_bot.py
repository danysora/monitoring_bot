import discord
import threading
import time
import random
import os
from discord.ext import commands
import gsmwarehouse  # Import the GSMWarehouse code
import backmarket  # Import the Backmarket code
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

intents = discord.Intents.default()
intents.message_content = True  # To access message content

bot = commands.Bot(command_prefix='!', intents=intents)

# Define a dictionary to store bot instances
bots = {
    "backmarket": backmarket,
    "gsmwarehouse": gsmwarehouse,
}

# Variable to track if a notification channel is set
notification_channel_id = 'channel_id_placeholder'

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='welcoming')
async def welcoming(ctx):
    welcome_message = "Greetings! I am Clappy, your dedicated assistant. Welcome to your exclusive monitoring server, meticulously designed to oversee Backmarket and GSMWarehouse for the products of your choice. Your CSV database will be diligently updated the moment any changes occur, and you will receive instant notifications."

    # Mention your bot's name
    bot_name = bot.user.name

    instructions = f"Allow me, {bot_name}, to assist you effectively. Should you require a comprehensive list of available commands, simply type '!custom_help.'"
    
    enjoy_message = "Indulge in the capabilities of your personalized bot and make the most of your experience!"

    # Combine the messages
    full_message = welcome_message + "\n\n" + instructions + "\n\n" + enjoy_message

    await ctx.send(full_message)


@bot.command(name='custom_help')
async def show_help(ctx):
    help_message = "Available commands:\n"
    
    # List of store names
    store_names = ", ".join(bots.keys())

    help_message += f"!welcoming - Welcome message from Clappy\n"
    help_message += f"!Backmarket - Use Backmarket commands\n"
    help_message += f"!GSMWarehouse - Use GSMWarehouse commands\n"
    help_message += f"!add_url [store] [url] - Add a URL for a specific store\n"
    help_message += f"!remove_url [store] [url] - Remove a URL for a specific store\n"
    help_message += f"!backmarket_database - Export Backmarket database\n"
    help_message += f"!gsm_database - Export GSMWarehouse database\n"
    help_message += f"!start_scraping [store] - Start scraping for a specific store or all stores\n"
    help_message += f"!stop_scraping [store] - Stop scraping for a specific store or all stores\n"

    # Append store-specific commands
    for store in bots:
        help_message += f"!{store.lower()}_add [url] - Add a {store} URL\n"
        help_message += f"!{store.lower()}_remove [url] - Remove a {store} URL\n"

    help_message += f"Available stores: {store_names}\n"
    help_message += "To learn more about a specific command, use `!help [command]`."

    await ctx.send(help_message)

@bot.command(name='Backmarket')
async def backmarket_clappy(ctx):
    if ctx.message.content == '!Backmarket':
        await ctx.send("Backmarket is currently operational")

@bot.command(name='GSMWarehouse')
async def gsm_clappy(ctx):
    if ctx.message.content == '!GSMWarehouse':
        await ctx.send("GSMWarehouse is currently operational")


@bot.command(name='add_url')
async def add_url(ctx, store, url: str):
    if store in bots:
        bot_instance = bots[store]
        added = bot_instance.add_url_to_user_urls(url)
        if added:
            await ctx.send(f"{url} was added to the database.")
        else:
            await ctx.send("Url may be invalid or duplicate.")
    else:
        await ctx.send("Invalid store name.")

@bot.command(name='remove_url')
async def remove_url(ctx, store, url: str):
    if store in bots:
        bot_instance = bots[store]
        removed = bot_instance.remove_url_from_user_urls(url)
        if removed:
            await ctx.send(f"{url} was removed from the database.")
        else:
            await ctx.send("URL not found in the database.")
    else:
        await ctx.send("Invalid store name.")

@bot.command(name='backmarket_database')
async def send_backmarket_database(ctx):
    try:
        if os.path.isfile("products.csv"):
            with open("products.csv", "rb") as file:
                await ctx.send("Here is the database for Backmarket:", file=discord.File(file, "products.csv"))
        else:
            await ctx.send("The database file 'products.csv' does not exist.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command(name='gsm_database')
async def send_gsm_database(ctx):
    try:
        if os.path.isfile("gsmwarehouse_products.csv"):
            with open("gsmwarehouse_products.csv", "rb") as file:
                await ctx.send("Here is the database for GSMWarehouse:", file=discord.File(file, "gsmwarehouse_products.csv"))
        else:
            await ctx.send("The database file 'gsmwarehouse_products.csv' does not exist.")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

# Define a global stop_signal variable
# Define a global stop_signal variable
global_stop_signal = threading.Event()

@bot.command(name='start_scraping')
async def start_scraping(ctx, store=None):
    if store:
        if store in bots:
            bot_instance = bots[store]
            scraper_thread = threading.Thread(target=bot_instance.scrape_and_update_product_data, args=(bot_instance.use_proxies, bot_instance.proxy_list))
            scraper_thread.daemon = True
            scraper_thread.start()
            await ctx.send(f"Scraping process for {store} has been started.")
        else:
            await ctx.send("Invalid store name.")
    else:
        for store in bots:
            bot_instance = bots[store]
            scraper_thread = threading.Thread(target=bot_instance.scrape_and_update_product_data, args=(bot_instance.use_proxies, bot_instance.proxy_list))
            scraper_thread.daemon = True
            scraper_thread.start()
            await ctx.send(f"Scraping process for {store} has been started.")

@bot.command(name='stop_scraping')
async def stop_scraping(ctx, store=None):
    if store:
        if store in bots:
            bot_instance = bots[store]
            bot_instance.stop_signal.set()
            await ctx.send(f"Scraping process for {store} has been stopped.")
        else:
            await ctx.send("Invalid store name.")
    else:
        for store in bots:
            bot_instance = bots[store]
            bot_instance.stop_signal.set()
            await ctx.send(f"Scraping process for {store} has been stopped.")

# This code uses the global_stop_signal variable within the context of Discord to control scraping across all stores.

file_modification_times = {
    "products.csv": 0,
    "gsmwarehouse_products.csv": 0,
}

# Directory to watch
watch_directory = os.path.abspath(os.path.dirname(__file__))  # Assumes the code is in the same directory as the CSV files

# ... Your previous code ...

# Initialize an observer to watch for file changes
observer = Observer()

# Define a global variable to store the last modification time for each file
file_modification_times = {
    "products.csv": 0,
    "gsmwarehouse_products.csv": 0,
}

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            file_name = os.path.basename(event.src_path)
            if file_name in file_modification_times:
                current_time = time.time()
                if current_time - file_modification_times[file_name] > 1:
                    file_modification_times[file_name] = current_time
                    bot.loop.create_task(send_file_update(event.src_path, file_name))

# Start the observer and add the event handler
observer.schedule(FileChangeHandler(), path=watch_directory)
observer.start()

# Function to send a message when a file is modified
async def send_file_update(file_path, file_name):
    try:
        with open(file_path, "rb") as file:
            channel = bot.get_channel(int(notification_channel_id))
            if channel:
                await channel.send(f"Database updated: {file_name}", file=discord.File(file, file_name))
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def scrape_and_update_all():
    while True:
        if global_stop_signal.is_set():
            time.sleep(1)
            continue

        for store in bots:
            bot_instance = bots[store]
            bot_instance.scrape_and_update_product_data(bot_instance.use_proxies, bot_instance.proxy_list)

        interval = random.uniform(5, 20)
        time.sleep(interval)

scraper_thread = threading.Thread(target=scrape_and_update_all)
scraper_thread.daemon = True
scraper_thread.start()

bot.run('bot_key_placeholder')
