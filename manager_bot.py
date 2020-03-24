from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from telegram import Update
from telegram import Bot
from telegram import ReplyKeyboardMarkup
from config_app import Config, owner_list, DbConfig
from database_interface import AdminInteraction, DbInterface
import logging
import subprocess
import psycopg2
from my_exceptions import AdminAccessException
import threading


token = ''  # bot token here
updater = Updater(token=token)
user_actions = {}

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class UserActions:
    set_message = "set_message"
    set_interval = "set_interval"


class UserKeyWords:
    set_message = "установить сообщение"
    stop_posting = "остановить постинг"
    start_posting = "начать постинг"
    set_interval = "установить интервал"


standard_menu = [[UserKeyWords.set_message], [UserKeyWords.start_posting], [UserKeyWords.stop_posting], [UserKeyWords.set_interval]]


def sender():
    subprocess.run([Config.sender_executor, Config.sender_file])


class TimerManager:
    main_timer = threading.Timer(Config.interval, sender)

    @classmethod
    def start(cls):
        threading.Thread(target=sender).start()
        cls.main_timer = threading.Timer(Config.interval, cls.start)
        cls.main_timer.start()

    @classmethod
    def stop(cls):
        cls.main_timer.cancel()


def test_case():
    TimerManager.start()


def start(bot: Bot, update: Update):
    print(update.message)
    bot.send_message(chat_id=update.message.chat_id, text="nigga")
    # subprocess.run(['python', 'sender_test.py'])
    if update.message.chat_id in owner_list:
        reply_markup = ReplyKeyboardMarkup(standard_menu)
        bot.send_message(chat_id=update.message.chat_id, text="выберите действие", reply_markup=reply_markup)


def message_handler(bot: Bot, update: Update):
    if user_actions.get(update.message.chat_id) == UserActions.set_message:
        try:
            user = AdminInteraction(owner_list)
            user.set_message_to_db(update.message.chat_id, update.message.text)
            bot.send_message(chat_id=update.message.chat_id, text="сообщение удачно установлено")
            print(user.get_message_from_db(update.message.chat_id))
        except AdminAccessException as exc:
            bot.send_message(exc)
        finally:
            del user_actions[update.message.chat_id]

    elif user_actions.get(update.message.chat_id) == UserActions.set_interval:
        try:
            try:
                assert update.message.chat_id in owner_list
                interval = int(update.message.text)
                Config.interval = interval
            except AssertionError:
                raise AdminAccessException("вы не админ")
            except ValueError:
                return bot.send_message(chat_id=update.message.chat_id, text="интервал должен быть цифрой")
        except AdminAccessException as ae:
            return bot.send_message(chat_id=update.message.chat_id, text=ae)
        finally:
            del user_actions[update.message.chat_id]
        bot.send_message(chat_id=update.message.chat_id, text="интервал успешно установлен")

    else:
        if update.message.chat_id in owner_list:
            if update.message.text == UserKeyWords.set_message:
                user_actions[update.message.chat_id] = UserActions.set_message
                bot.send_message(chat_id=update.message.chat_id, text="отправьте своё сообщение")
            elif update.message.text == UserKeyWords.start_posting:
                TimerManager.start()
                bot.send_message(chat_id=update.message.chat_id, text="постинг начат")
            elif update.message.text == UserKeyWords.stop_posting:
                TimerManager.stop()
                bot.send_message(chat_id=update.message.chat_id, text="постинг остановлен")
            elif update.message.text == UserKeyWords.set_interval:
                user_actions[update.message.chat_id] = UserActions.set_interval
                bot.send_message(chat_id=update.message.chat_id, text="отправьте интервал в секундах")
        else:
            bot.send_message(chat_id=update.message.chat_id, text="вы не админ")


dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

if __name__ == "__main__":
    DATABASE_URL = DbConfig.DATABASE_URL
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    conn.autocommit = True
    cursor = conn.cursor()
    DbInterface().create_default_table(cursor)
    cursor.close()
    conn.close()
    updater.start_polling()
