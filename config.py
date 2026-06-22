import os

import dotenv
dotenv.load_dotenv()

telegram_token = os.getenv("TELEGRAM_API_TOKEN")
arolink_shortner_api_key = os.getenv("AROLINKS_SHORTNER_API")
viplink_shortner_api_key = os.getenv("VIPLINK_SHORTNER_API")
google_sheets_api_key = os.getenv("APP_SCRIPT_URL")