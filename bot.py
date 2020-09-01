import telebot

from modules.buttons import *
from modules.content import *
from modules.database import *
from modules.menu import *
from modules.parse_functions import *


class Bot:
    def __init__(self,
                 tgbot=telebot.TeleBot(token=TOKEN),
                 menu=MainMenu(),
                 database=None):
        self.tgbot = tgbot
        self.menu = menu
        self.database = database

    def check_user_is_follower(self, user_id):
        channel = self.tgbot.get_chat_member(chat_id=CHANNEL, user_id=user_id)
        if "'status': 'left'" in str(channel):
            return 0
        return 1

    def create_user_from_start_user_message(self, user_message):
        telegram_id = user_message.chat.id
        inviter = get_inviter(user_message)
        self.treat_inviter(inviter)
        is_follower = self.check_user_is_follower(telegram_id)
        user = User(telegram_id=telegram_id,
                    is_follower=is_follower,
                    invited_by=inviter)
        self.database.add_user(user)
        return user

    def change_balance(self, user: User, receiver: int, value: float):
        receiver = self.database.get_user_by_telegram_id(receiver)
        self.database.change_balance(receiver, value)
        self.tgbot.send_message(receiver.telegram_id,
                                text=f'Ваш баланс изменил админ!\nНовый баланс: {receiver.balance}')
        self.tgbot.send_message(user.telegram_id,
                                text=f'Новый баланс пользователя: {receiver.balance}')

    def get_user(self, user_message):
        user = self.database.get_user_by_telegram_id(telegram_id=user_message.chat.id)
        if user is not None:
            return user
        else:
            user = self.create_user_from_start_user_message(user_message)
            return user

    def get_user_by_id(self, user_id):
        return self.database.get_user_by_telegram_id(user_id)

    def treat_inviter(self, inviter):
        try:
            inviter = self.database.get_user_by_telegram_id(inviter)
            if inviter is not None:
                self.database.change_balance(inviter, MONEY_FOR_INVITE)
        except Exception as er:
            print(er)

    def treat_seller(self, user: User):
        self.database.change_balance(user, MONEY_FOR_SALE)

    def sold_access(self, user):
        invited_users = self.database.get_invited_users(user)
        sold_access = False
        if invited_users is not None:
            for invited_user in invited_users:
                if self.check_user_is_follower(invited_user.telegram_id):
                    self.treat_seller(user)
                    sold_access = True
        return sold_access

    def send_start(self, user: User):
        self.tgbot.send_message(chat_id=user.telegram_id, text=MESSAGES['start'], reply_markup=INFORMATION_KEYBOARD)
        self.tgbot.send_message(chat_id=user.telegram_id, text=MESSAGES['menu'], reply_markup=self.menu.get_menu())

    def send_buy(self, user: User):
        if not user.is_follower:
            self.tgbot.send_message(chat_id=user.telegram_id,
                                    text=MESSAGES['buy'],
                                    reply_markup=BUY_BUTTON)
        else:
            self.tgbot.send_message(chat_id=user.telegram_id,
                                    text=MESSAGES['payed'])

    def send_preview(self, user: User):
        self.tgbot.send_message(chat_id=user.telegram_id,
                                text=MESSAGES['preview'],
                                reply_markup=PREVIEW_BUTTON)

    def send_suggest(self, user: User):
        self.tgbot.send_message(chat_id=user.telegram_id,
                                text=MESSAGES['suggest'],
                                reply_markup=SUGGESTION_RULES_BUTTON)

    def send_partner(self, user: User):
        self.tgbot.send_message(chat_id=user.telegram_id,
                                text=MESSAGES['partner'],
                                reply_markup=PARTNERSHIP_RULES_BUTTON)

    def send_personal_cabinet(self, user: User):
        text = get_personal_cabinet_message(user)
        self.tgbot.send_message(chat_id=user.telegram_id, text=text + MESSAGES['refresh'],
                                reply_markup=PERSONAL_CABINET_KEYBOARD,
                                disable_web_page_preview=True)

    def send_refresh(self, user: User, message_id):
        text = get_personal_cabinet_message(user)
        self.tgbot.edit_message_text(text=text + MESSAGES['refreshed'], chat_id=user.telegram_id, message_id=message_id,
                                     reply_markup=PERSONAL_CABINET_KEYBOARD,
                                     disable_web_page_preview=True)

    def send_message(self, telegram_id, message):
        self.tgbot.send_message(telegram_id, message)

    def send_all(self, user: User, message):
        receivers = self.database.get_all_users()
        for receiver in receivers:
            self.send_message(receiver.telegram_id, message)
        self.send_message(user.telegram_id, 'Рассылка закончена!')

    def send_statistics(self, user: User):
        statistics_message = self.database.get_statistics_message()
        self.tgbot.send_message(user.telegram_id, statistics_message)


bot = Bot()


@bot.tgbot.message_handler(commands=['start',
                                     'buy',
                                     'preview',
                                     'suggest',
                                     'partner',
                                     'change_balance',
                                     'statistics',
                                     'send_all'])
def commands_executor(user_message):
    bot.database = DataBase(db_file='database.db')
    user = bot.get_user(user_message)
    if 'start' in user_message.text:
        bot.send_start(user)
    if 'buy' in user_message.text:
        bot.send_buy(user)
    if 'preview' in user_message.text:
        bot.send_preview(user)
    if 'suggest' in user_message.text:
        bot.send_suggest(user)
    if 'partner' in user_message.text:
        bot.send_partner(user)
    if 'personal_cabinet' in user_message.text:
        bot.send_personal_cabinet(user)
    if 'change_balance' in user_message.text and user.telegram_id == ADMIN_ID:
        receiver = get_receiver(user_message)
        value = get_value(user_message)
        if receiver.isdigit():
            bot.change_balance(user=user, receiver=receiver, value=value)
    if 'send_all' in user_message.text and user.telegram_id == ADMIN_ID:
        message = get_message_from_send_all(user_message)
        bot.send_all(user, message)

    if 'statistics' in user_message.text and user.telegram_id == ADMIN_ID:
        bot.send_statistics(user)


@bot.tgbot.message_handler(content_types=['text'])
def keyboard_handler(user_message):
    bot.database = DataBase(db_file='database.db')
    user = bot.get_user(user_message)
    if bot.menu.sent_by_menu(user_message.text):
        if user_message.text == bot.menu.MENU_BUTTONS['buy']:
            bot.send_buy(user)
        if user_message.text == bot.menu.MENU_BUTTONS['preview']:
            bot.send_preview(user)
        if user_message.text == bot.menu.MENU_BUTTONS['suggest']:
            bot.send_suggest(user)
        if user_message.text == bot.menu.MENU_BUTTONS['partner']:
            bot.send_partner(user)
        if user_message.text == bot.menu.MENU_BUTTONS['personal_cabinet']:
            bot.send_personal_cabinet(user)


@bot.tgbot.callback_query_handler(func=lambda x: True)
def query_handler(call):
    bot.database = DataBase(db_file='database.db')
    user = bot.get_user_by_id(call.from_user.id)
    if call.data == 'refresh':
        if bot.sold_access(user):
            bot.send_refresh(user, call.message.message_id)


try:
    bot.tgbot.polling()
except Exception as er:
    print(er)
    bot.send_message(849014162, er)
