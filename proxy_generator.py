import json

# Open the text file for reading
with open("http_proxies.txt", "r") as file:
    lines = file.readlines()

# Remove any leading or trailing whitespace from each line
proxies = [line.strip() for line in lines]

# Create a dictionary in the JSON format
proxy_data = {"proxies": proxies}

# Convert the dictionary to a JSON string
json_data = json.dumps(proxy_data, indent=2)

# Save the JSON data to a file
with open("http_proxies.json", "w") as json_file:
    json_file.write(json_data)

print("Proxies have been converted to JSON and saved to 'http_proxies.json'.")