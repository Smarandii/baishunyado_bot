from modules.models import User
from modules.content import MESSAGES


def get_statistics_message(u_a, f_a, i_a):
    return f'Количество пользователей бота: {u_a}\nКоличество подписчиков канала: {f_a}\nКоличество приглашённых: {i_a}'


def get_receiver(user_message):
    return user_message.text.replace('/change_balance ', '').split()[0]


def get_value(user_message):
    return user_message.text.replace('/change_balance ', '').split()[1]


def get_message_from_send_all(user_message):
    return user_message.text.replace('/send_all ', '')


def get_inviter(user_message):
    inviter = 'None'
    if 'start ' in user_message.text:
        inviter = user_message.text.replace('/start ', '')
        print(inviter)
    return inviter


def get_personal_cabinet_message(user: User) -> str:
    if user.is_follower:
        permission = '✅'
    else:
        permission = '❌'
    text = \
f"""\
Доступ к каналу: {permission}
Баланс: {user.balance} руб.
Реферальная ссылка: {user.get_partnership_link()}

Вывод денежных средств с баланса доступен только подписанным на канал пользователям!
Минимальная сумма вывода 30 рублей.
"""
    return text
