import requests
import config
api_token_arolink = config.arolink_shortner_api_key

def arolinks_shortner(destination_url):
    api_url = "https://arolinks.com/api"

    # Simply omit the 'alias' key from the payload dictionary
    payload = {
        'api': api_token_arolink,
        'url': destination_url
    }

    try:
        response = requests.get(api_url, params=payload)
        response.raise_for_status()

        result = response.json()

        if result.get("status") == "error":
            return f"Error: {result.get('message')}"
        else:
            return f"{result.get('shortenedUrl')}"

    except requests.exceptions.RequestException as e:
        return f"An HTTP error occurred: {e}"





# Define your parameters
api_token_vipurl = config.viplink_shortner_api_key


# Define the base URL and the payload dictionary
# (Omitting 'alias' as requested earlier)
def viplinks_url_shortner(destination_url):
    api_url = "https://vplink.in/api"
    payload = {
        'api': api_token_vipurl,
        'url': destination_url
    }

    try:
        # Send the GET request
        response = requests.get(api_url, params=payload)
        response.raise_for_status()  # Raises an error for bad HTTP statuses

        # Parse the JSON response
        result = response.json()

        if result.get("status") == "error":
            return f"Error: {result.get('message')}"
        else:
            return f"{result.get('shortenedUrl')}"

    except requests.exceptions.RequestException as e:
        return f"An HTTP error occurred: {e}"