from config import telegram_token
from telebot import TeleBot
from datetime import datetime
import urllib.parse
import process
import link_changer
import shortner
import data_uploader

bot = TeleBot(telegram_token)

# Thread/chat-safe in-memory state dictionary
user_data = {}

def get_user_state(chat_id):
    if chat_id not in user_data:
        user_data[chat_id] = {}
    return user_data[chat_id]

def clear_user_state(chat_id):
    if chat_id in user_data:
        del user_data[chat_id]

def is_valid_url(url):
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def handle_command_interrupt(message):
    """
    Checks if the user typed a command instead of the requested input.
    If so, clears state/handlers and routes/cancels accordingly.
    """
    if message.text and message.text.startswith('/'):
        command = message.text.split()[0].lower()
        if command == '/cancel':
            bot.clear_step_handlers_by_chat_id(message.chat.id)
            clear_user_state(message.chat.id)
            bot.send_message(message.chat.id, "❌ Operation cancelled. You can start again with /createmessage.")
            return True
        elif command == '/start':
            bot.clear_step_handlers_by_chat_id(message.chat.id)
            clear_user_state(message.chat.id)
            send_welcome(message)
            return True
        elif command == '/createmessage':
            bot.clear_step_handlers_by_chat_id(message.chat.id)
            clear_user_state(message.chat.id)
            create_message(message)
            return True
        else:
            bot.clear_step_handlers_by_chat_id(message.chat.id)
            clear_user_state(message.chat.id)
            bot.send_message(message.chat.id, "❌ Process aborted because a new command was entered. Use /createmessage to start over.")
            return True
    return False


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        f"Hello {message.from_user.first_name}! Movie Message Generator Bot is ready.\n\n"
        "Commands:\n"
        "/createmessage - Start generating a movie download post\n"
        "/cancel - Abort current creation process"
    )


@bot.message_handler(commands=['cancel'])
def cancel_command(message):
    bot.clear_step_handlers_by_chat_id(message.chat.id)
    clear_user_state(message.chat.id)
    bot.send_message(message.chat.id, "❌ There is no active process to cancel.")


@bot.message_handler(commands=['createmessage'])
def create_message(message):
    bot.clear_step_handlers_by_chat_id(message.chat.id)
    clear_user_state(message.chat.id)
    msg = bot.send_message(message.chat.id, "🎬 Enter the link of your movie / video:")
    bot.register_next_step_handler(msg, get_link)


def get_link(message):
    if handle_command_interrupt(message):
        return

    url = message.text.strip()
    
    # Validate general URL format
    if not is_valid_url(url):
        msg = bot.send_message(
            message.chat.id, 
            "⚠️ That does not look like a valid link. Please enter a valid URL (starting with http:// or https://):"
        )
        bot.register_next_step_handler(msg, get_link)
        return

    # Check for Google Drive URL and convert
    if "drive.google.com" in url:
        direct_link = link_changer.drive_to_direct(url)
        if direct_link is None:
            msg = bot.send_message(
                message.chat.id,
                "⚠️ Invalid Google Drive link format.\n"
                "Please make sure it's a shareable link in `/file/d/FILE_ID/` or `id=FILE_ID` format, or enter another link:"
            )
            bot.register_next_step_handler(msg, get_link)
            return
    else:
        # Accept external direct link as-is
        direct_link = url

    state = get_user_state(message.chat.id)
    state['direct_link'] = direct_link

    msg = bot.send_message(message.chat.id, "📝 Enter the name of the movie / video:")
    bot.register_next_step_handler(msg, get_name)


def get_name(message):
    if handle_command_interrupt(message):
        return

    state = get_user_state(message.chat.id)
    state['name'] = message.text.strip()

    msg = bot.send_message(message.chat.id, "📅 Enter the release year (e.g. 2024):")
    bot.register_next_step_handler(msg, get_year)


def get_year(message):
    if handle_command_interrupt(message):
        return

    state = get_user_state(message.chat.id)
    state['year'] = message.text.strip()

    msg = bot.send_message(message.chat.id, "⭐ Enter the rating (e.g. 8.2):")
    bot.register_next_step_handler(msg, get_rating)


def get_rating(message):
    if handle_command_interrupt(message):
        return

    state = get_user_state(message.chat.id)
    state['rating'] = message.text.strip()

    msg = bot.send_message(message.chat.id, "🌐 Enter the language(s) (e.g. Hindi | English):")
    bot.register_next_step_handler(msg, get_language)


def get_language(message):
    if handle_command_interrupt(message):
        return

    state = get_user_state(message.chat.id)
    state['language'] = message.text.strip()

    msg = bot.send_message(message.chat.id, "📦 Enter the quality (e.g. 720p HDRip):")
    bot.register_next_step_handler(msg, get_quality)


def get_quality(message):
    if handle_command_interrupt(message):
        return

    state = get_user_state(message.chat.id)
    state['quality'] = message.text.strip()

    procesing(message)


def procesing(message):
    chat_id = message.chat.id
    state = get_user_state(chat_id)

    if 'direct_link' not in state:
        bot.send_message(chat_id, "❌ Error: session state lost. Please start again using /createmessage.")
        clear_user_state(chat_id)
        return

    status_msg = bot.send_message(chat_id, "⏳ Generating shortened links. Please wait...")

    direct_link = state['direct_link']
    name = state['name']
    year = state['year']
    rating = state['rating']
    language = state['language']
    quality = state['quality']

    # 1. Shorten Links
    link_A = shortner.arolinks_shortner(direct_link)
    # If shortening fails (returns Error string), fall back to direct link
    if link_A.startswith("Error"):
        link_A_display = direct_link
        print(f"⚠️ Arolinks error for {chat_id}: {link_A}. Used direct link fallback.")
    else:
        link_A_display = link_A

    link_B = shortner.viplinks_url_shortner(direct_link)
    if link_B.startswith("Error"):
        link_B_display = direct_link
        print(f"⚠️ Viplinks error for {chat_id}: {link_B}. Used direct link fallback.")
    else:
        link_B_display = link_B

    # 2. Format final download template
    # Note: Link 1 maps to VipLinks (link_B_display) and Link 2 to AroLinks (link_A_display) in process_data
    output_text = process.process_data(link_A_display, link_B_display, name, year, rating, language, quality)

    # 3. Send output to user
    bot.send_message(chat_id, output_text)

    # Delete processing status message
    try:
        bot.delete_message(chat_id, status_msg.message_id)
    except Exception:
        pass

    # 4. Upload data to Google Sheets spreadsheet
    now = datetime.now()
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name

    upload_success = data_uploader.send_to_spreadsheet(
        direct_link,
        link_B,
        link_A,
        name,
        year,
        rating,
        language,
        quality,
        str(now.date()),
        now.strftime("%H:%M:%S"),
        firstname,
        lastname,
        chat_id
    )

    if upload_success:
        bot.send_message(chat_id, "✅ Details saved to Google Sheets successfully.")
    else:
        bot.send_message(chat_id, "⚠️ Warning: Details could not be saved to Google Sheets (check server log).")

    # Clean up user session
    clear_user_state(chat_id)


bot.polling(non_stop=True)