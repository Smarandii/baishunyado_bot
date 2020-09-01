from telebot import types


class Menu:
    MENU_BUTTONS = {
    }

    def __init__(self):
        pass

    def sent_by_menu(self, text):
        if text in self.MENU_BUTTONS.values():
            return True
        return False


class MainMenu(Menu):
    MENU_BUTTONS = {
        'buy': 'Купить доступ 🥬',
        'preview': 'Предпросмотр контента 🍓',
        'suggest': 'Предложить пост 🍒',
        'partner': 'Партнёрка 🍇',
        'personal_cabinet': 'Личный кабинет 🍌'
    }

    def get_menu(self):
        buy_btn = types.KeyboardButton(text=self.MENU_BUTTONS['buy'])
        preview_btn = types.KeyboardButton(text=self.MENU_BUTTONS['preview'])
        suggest_btn = types.KeyboardButton(text=self.MENU_BUTTONS['suggest'])
        partner_btn = types.KeyboardButton(text=self.MENU_BUTTONS['partner'])
        personal_cabinet_btn = types.KeyboardButton(text=self.MENU_BUTTONS['personal_cabinet'])
        keyboard = types.ReplyKeyboardMarkup()
        keyboard.row(buy_btn, preview_btn)
        keyboard.row(suggest_btn, partner_btn, personal_cabinet_btn)
        return keyboard
