import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('db.db')
        self.cursor = self.connection.cursor()

    # основная таблица
    def create_table(self):
        with self.connection:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    collection_name TEXT,
                                    name TEXT,
                                    author TEXT,
                                    fee INTEGER,
                                    url TEXT
                                )''')

    # добавить проект
    def add_data(self, collection_name, name, author, fee, url):
        with self.connection:
            self.cursor.execute('INSERT INTO projects VALUES (NULL, ?, ?, ?, ?, ?)',
                                (collection_name, name, author, fee, url))

    # получить проект
    def get_project(self, collection_name):
        with self.connection:
            return self.cursor.execute(
                'SELECT collection_name, name, author, fee, url FROM projects WHERE collection_name=?',
                (collection_name,)).fetchone()

    # получить все проекты
    def get_all_project(self):
        with self.connection:
            return self.cursor.execute('SELECT collection_name FROM projects').fetchall()

    # количество коллекций
    def collection_count(self):
        with self.connection:
            return self.cursor.execute('SELECT COUNT(*) FROM projects').fetchone()

    # удалить проект
    def delete_project(self, name):
        with self.connection:
            self.cursor.execute('DELETE FROM projects WHERE collection_name=?', (name,))

    # таблица пользователей
    def create_user_table(self):
        with self.connection:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id INTEGER,
                                    status INTEGER
                                )''')

    # добавить пользователя
    def add_user(self, user_id, status):
        with self.connection:
            self.cursor.execute('INSERT INTO users VALUES (NULL, ?, ?)', (user_id, status,))

    # обновить статус
    def change_status(self, user_id, status):
        with self.connection:
            self.cursor.execute('UPDATE users SET status={} WHERE user_id=?'.format(status), (user_id,))

    # получить пользователей для рассылки
    def get_users(self, status):
        with self.connection:
            return self.cursor.execute('SELECT user_id FROM users WHERE status=?', (status,)).fetchall()

    # получить пользователя
    def get_user(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchone()

    # удалить пользовтеля
    def del_user(self, user_id):
        with self.connection:
            self.cursor.execute('DELETE FROM users WHERE user_id=?', (user_id,))
