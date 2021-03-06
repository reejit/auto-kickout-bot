import configparser, logging, traceback
from telegram.ext import Updater, Filters, MessageHandler


# Config
config = configparser.ConfigParser()
config.read('config.ini')


# Log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(funcName)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Error Callback
def error_callback(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def kickout(update, context):
    try:
        for new_user in update.effective_message.new_chat_members:
            update.effective_chat.kick_member(user_id=new_user.id)
        for new_user in update.effective_message.new_chat_members:
            update.effective_chat.unban_member(user_id=new_user.id)
        update.effective_message.delete()
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())


def remove_kickout_msg(update, context):
    try:
        update.effective_message.delete()
    except Exception as e:
        logger.error(e)
        logger.debug(traceback.format_exc())


def main():
    updater = Updater(config['BOT']['accesstoken'], use_context=True)
    dp = updater.dispatcher
    dp.add_error_handler(error_callback)

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, kickout))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, remove_kickout_msg))
    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
