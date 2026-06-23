import requests
import config

api_token_arolink = config.arolink_shortner_api_key
api_token_vipurl = config.viplink_shortner_api_key

def arolinks_shortner(destination_url):
    if not api_token_arolink:
        return "Error: Arolink API key not set"

    api_url = "https://arolinks.com/api"
    payload = {
        'api': api_token_arolink,
        'url': destination_url
    }

    try:
        response = requests.get(api_url, params=payload, timeout=10)
        response.raise_for_status()

        result = response.json()
        if result.get("status") == "error":
            return f"Error: {result.get('message')}"
        else:
            return f"{result.get('shortenedUrl')}"

    except requests.exceptions.RequestException as e:
        return f"Error: HTTP request failed: {e}"
    except Exception as e:
        return f"Error: {e}"


def viplinks_url_shortner(destination_url):
    if not api_token_vipurl:
        return "Error: Viplink API key not set"

    api_url = "https://vplink.in/api"
    payload = {
        'api': api_token_vipurl,
        'url': destination_url
    }

    try:
        response = requests.get(api_url, params=payload, timeout=10)
        response.raise_for_status()

        result = response.json()
        if result.get("status") == "error":
            return f"Error: {result.get('message')}"
        else:
            return f"{result.get('shortenedUrl')}"

    except requests.exceptions.RequestException as e:
        return f"Error: HTTP request failed: {e}"
    except Exception as e:
        return f"Error: {e}"