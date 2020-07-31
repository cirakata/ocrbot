try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from telegram import Update, Bot, ParseMode
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! \n\nWelcome to Optical Character Recognizer Bot. \n\nJust send a clear image to the bot and it will recognize the text in the image and send it as a message!\nTo get my contact details tap /contact \nTo get donation details tap /donate\n')

def contact(bot, update):
    """Send a message when the command /contact is issued."""
    update.message.reply_text("Heya! You can find me on \n[Telegram](https://telegram.me/nitishjeet7)", parse_mode=ParseMode.MARKDOWN)

def search(bot, update):
    """Send reply of user's message."""
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('testing.jpg')
    try:
        output=pytesseract.image_to_string(Image.open('testing.jpg'))
        update.message.reply_text('`'+str(output)+'`',parse_mode=ParseMode.MARKDOWN,reply_to_message_id=update.message.message_id)
    except Exception as e:
        update.message.reply_text(e)
        try:
            os.remove('testing.jpg')
        except Exception:
            pass

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start the bot."""
    ocr_bot_token=os.environ.get("BOT_TOKEN")
    updater = Updater(ocr_bot_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("contact", contact))
    dp.add_handler(MessageHandler(Filters.photo, search))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
