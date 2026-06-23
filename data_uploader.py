import requests
import config

# Paste your Google Apps Script Web App URL here
WEB_APP_URL = config.google_sheets_api_key

def send_to_spreadsheet(
        direct_link, vipurl_link, arolinks_link, name, year,
        rating, language, quality, date, time, firstname, lastname, chat_id
):
    """
    Accepts individual variables directly as arguments and sends them to Google Sheets.
    """
    if not WEB_APP_URL:
        print("❌ Spreadsheet upload skipped: APP_SCRIPT_URL not configured in .env")
        return False

    # Map your individual variables straight to the JSON keys expected by Apps Script
    data_payload = {
        "direct_link": direct_link,
        "vipurl_link": vipurl_link,
        "arolinks_link": arolinks_link,
        "name": name,
        "year": year,
        "rating": rating,
        "language": language,
        "quality": quality,
        "date": date,
        "time": time,
        "firstname": firstname or "",
        "lastname": lastname or "",
        "chat_id": str(chat_id)  # Standardize chat ID as a string
    }

    try:
        # Send data via POST request with a timeout
        response = requests.post(WEB_APP_URL, json=data_payload, timeout=10)
        response.raise_for_status()
        result = response.json()

        if result.get("status") == "success":
            print("✅ Data successfully saved to spreadsheet.")
            return True
        else:
            print(f"❌ Apps Script Error: {result.get('message')}")
            return False

    except Exception as e:
        print(f"❌ Failed to connect to the spreadsheet: {e}")
        return False