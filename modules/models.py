from modules.content import BOT_TAG


class User:
    def __init__(self, db_id=None, telegram_id=None, balance=0, is_follower: int = 0, invited_by: str = 'None'):
        self.db_id = db_id
        self.telegram_id = telegram_id
        self.balance = balance
        self.is_follower = is_follower
        self.invited_by = invited_by

    def __str__(self):
        return f"{self.db_id}, {self.telegram_id}, {self.balance}, {self.is_follower}, {self.invited_by}"

    def list_for_db(self):
        return str(self.telegram_id), int(self.balance), int(self.is_follower), str(self.invited_by)

    def get_partnership_link(self):
        partnership_link = fr'https://t.me/{BOT_TAG}?start={self.telegram_id}'
        return partnership_link
