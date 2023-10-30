import csv
import cloudscraper
from bs4 import BeautifulSoup
import json
import random
import time

scraped_urls = set()

# Create user URLs and product data JSON files if they don't exist
with open('gsmwarehouse_user_urls.json', 'a+') as user_urls_file:
    user_urls_file.seek(0)
    user_urls_content = user_urls_file.read()
    if not user_urls_content:
        user_urls_file.write('[]')

with open('gsmwarehouse_products.json', 'a+') as products_file:
    products_file.seek(0)
    products_content = products_file.read()
    if not products_content:
        products_file.write('[]')

# Load user URLs from 'gsmwarehouse_user_urls.json'
def load_user_urls():
    try:
        with open('gsmwarehouse_user_urls.json', 'r') as json_file:
            user_urls = json.load(json_file)
        return user_urls
    except FileNotFoundError:
        return []

# Browser configuration
browser_config = {
    'browser': 'chrome',  # You can change this to 'firefox' if needed
    'mobile': False,       # You can set this to False for desktop User-Agents
    'desktop': True,      # You can set this to False for mobile User-Agents
    'platform': 'windows' # You can change the platform as needed
}

scraper = cloudscraper.create_scraper(browser=browser_config)

# Function to scrape product information
def scrape_product_info(url, use_proxies, proxy_list):
    try:
        if use_proxies:
            # Select a random proxy from the list
            random_proxy = random.choice(proxy_list)
            proxies = {
                "http": f"http://{random_proxy}",
                "https": f"http://{random_proxy}",
            }
        else:
            proxies = None

        # Send a GET request to the URL using the user agent and proxy
        response = scraper.get(url, proxies=proxies)
        response.raise_for_status()

        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title from the <title> element
        title = soup.find('title').get_text()

        # Extract the price from the <tr> element with class and data-price attribute
        price_element = soup.find('tr', class_='31169 instock is_purchasable')
        price = price_element['data-price'] if price_element else 'Price not found'

        # Extract the stock status from the <td> element
        stock_element = soup.find('td', class_='stockcol', attrs={'data-label': 'Stock'})
        stock_text = stock_element.find('span', class_='instock').get_text() if stock_element else 'Stock status not found'
        
        availability = "In stock" if "InStock" in stock_text else "Out of stock"

        return title, price, availability
    except Exception as e:
        print(f"Error: {e}")
        return None
    
def add_url_to_user_urls(url):
    if 'gsmwarehouse.com' in url:
        user_urls = load_user_urls()
        if url not in user_urls:
            user_urls.append(url)
            with open('gsmwarehouse_user_urls.json', 'w') as json_file:
                json.dump(user_urls, json_file, indent=4)
            return True
        else:
            return False
    else:
        return False

def remove_url_from_user_urls(url):
    user_urls = load_user_urls()

    if url in user_urls:
        user_urls.remove(url)
        with open('gsmwarehouse_user_urls.json', 'w') as json_file:
            json.dump(user_urls, json_file, indent=4)
        return True
    else:
        return False


# Function to scrape and update product data
def scrape_and_update_product_data(use_proxies, proxy_list):
    user_urls = load_user_urls()
    if not user_urls:
        # No URLs to scrape. Waiting for user input...
        delay = random.uniform(5, 20)
        time.sleep(delay)
        return

    product_data = []

    # Load existing product data from 'gsmwarehouse_products.json' if it exists
    try:
        with open('gsmwarehouse_products.json', 'r') as json_file:
            product_data = json.load(json_file)
    except FileNotFoundError:
        pass

    updated = False  # Flag to track if any updates occurred

    for url in user_urls:
        # Check if the URL is already in the set of scraped URLs
        if url in scraped_urls:
            continue

        # Check if the URL is already in the product data
        existing_product = next((p for p in product_data if p['url'] == url), None)

        product_info = scrape_product_info(url, use_proxies, proxy_list)

        if product_info:
            title, price, availability = product_info

            if existing_product:
                # Check if there are differences in the data
                if (
                    existing_product['title'] != title
                    or existing_product['price'] != price
                    or existing_product['availability'] != availability
                ):
                    print(f"Updated Product Information for {url}:")
                    print(f"Title: {existing_product['title']} -> {title}")
                    print(f"Price: {existing_product['price']} -> {price}")
                    print(f"Availability: {existing_product['availability']} -> {availability}")

                    existing_product['title'] = title
                    existing_product['price'] = price
                    existing_product['availability'] = availability
                    updated = True
            else:
                print(f"New Product Scraped: {url}")
                product_data.append({'url': url, 'title': title, 'price': price, 'availability': availability})
                scraped_urls.add(url)  # Add the scraped URL to the set
                updated = True

    if updated:
        # Export to JSON
        with open('gsmwarehouse_products.json', 'w') as json_file:
            json.dump(product_data, json_file, indent=4)

        # Export to CSV
        with open('gsmwarehouse_products.csv', 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['ID', 'Type', 'SKU', 'Name', 'Published', 'Is featured?', 'Visibility in catalog', 'Short description']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for product in product_data:
                published = 1 if product['availability'] == 'In stock' else 0
                writer.writerow({
                    'ID': random.randint(1000, 9999),  # Random ID
                    'Type': 'variable',
                    'SKU': '',  # Empty SKU
                    'Name': product['title'],  # Use 'title' for Name
                    'Published': published,
                    'Is featured?': 0,
                    'Visibility in catalog': published,
                    'Short description': f"{product['title']} refurbished"  # Use 'title' for Short description
                })

# Remove the user input for proxy usage and related code
# use_proxies = input("Do you want to use proxies? (y/n): ").strip().lower() == 'y'
use_proxies = False  # Default to not using proxies

if use_proxies:
    # Load proxies from 'http_proxies.json'
    try:
        with open('http_proxies.json', 'r') as json_file:
            proxy_data = json.load(json_file)
        proxy_list = proxy_data.get('proxies', [])
    except FileNotFoundError:
        proxy_list = []
else:
    proxy_list = []

# Commented out the threading part
# # Create a thread for the scraping and updating
# scraper_thread = threading.Thread(target=scrape_and_update_product_data, args=(use_proxies, proxy_list))
# scraper_thread.daemon = True
# scraper_thread.start()

# Keep the main program running to allow the script to be run directly
# while True:
#     pass
