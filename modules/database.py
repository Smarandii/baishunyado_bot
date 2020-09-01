import sqlite3
from sqlite3 import Error

from modules.models import User
from modules.parse_functions import get_statistics_message


class DataBase:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_connection()
        self.c = self._get_connection()
        self.create_tables()

    def create_connection(self):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def _get_connection(self) -> sqlite3.connect:
        c = sqlite3.connect(self.db_file)
        return c

    def _select_all(self):
        with self.c:
            cursor = self.c.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
        return users

    def create_tables(self):
        with self.c:
            sql = '''\
            CREATE TABLE IF NOT EXISTS users \
            (id integer PRIMARY KEY, telegram_id text, balance bigint, is_follower integer, invited_by text)'''
            self.c.execute(sql)

    def add_user(self, user: User):
        with self.c:
            cursor = self.c.cursor()
            if self.get_user_by_telegram_id(telegram_id=user.telegram_id) is None:
                sql = f'INSERT INTO users(telegram_id, balance, is_follower, invited_by) VALUES(?,?,?,?)'
                cursor.execute(sql, user.list_for_db())
                self.c.commit()
            else:
                print('User already exists')

    def get_user_by_telegram_id(self, telegram_id: int) -> User or None:
        rows = self._select_all()
        for row in rows:
            user = User(db_id=row[0], telegram_id=row[1], balance=row[2], is_follower=row[3], invited_by=row[4])
            if int(user.telegram_id) == int(telegram_id):
                return user
        return None

    def update_user(self, user: User):
        with self.c:
            cursor = self.c.cursor()
            cursor.execute(f'UPDATE users '
                           f'SET telegram_id = ?, balance = ?, is_follower = ?, invited_by = ? '
                           f'WHERE telegram_id = {user.telegram_id}', user.list_for_db())
            self.c.commit()

    def change_balance(self, user: User, value: float):
        with self.c:
            user.balance = user.balance + float(value)
            self.update_user(user=user)

    def get_invited_users(self, invitor: User):
        invited_users = []
        rows = self._select_all()
        for row in rows:
            user = User(db_id=row[0], telegram_id=row[1], balance=row[2], is_follower=row[3], invited_by=row[4])
            print(invitor, ':', user)
            try:
                if int(invitor.telegram_id) == int(user.invited_by):
                    user.invited_by = 'None'
                    self.update_user(user)
                    invited_users.append(user)
            except Exception as er:
                print(er)
        return invited_users

    def get_statistics_message(self):
        users = self._select_all()
        users_amount = 0
        followers_amount = 0
        invited_amount = 0
        for user in users:
            user = User(db_id=user[0],
                        telegram_id=user[1],
                        balance=user[2],
                        is_follower=user[3],
                        invited_by=user[4])
            if user.is_follower:
                followers_amount += 1
            if user.invited_by != 'None':
                invited_amount += 1
            users_amount += 1
        return get_statistics_message(users_amount, followers_amount, invited_amount)

    def get_all_users(self) -> list:
        all_users = []
        users = self._select_all()
        for user in users:
            user = self._get_user_from_db(user)
            all_users.append(user)
        return all_users

    def print(self):
        rows = self._select_all()
        for row in rows:
            print(row)

    def _get_user_from_db(self, row) -> User:
        user = User(db_id=row[0], telegram_id=row[1], balance=row[2], is_follower=row[3], invited_by=row[4])
        return user


if __name__ == '__main__':
    db = DataBase(db_file='database.db')
    db.print()



