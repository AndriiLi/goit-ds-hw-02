import random

from faker import Faker
from src.config import DATABASE, USER, PASSWORD, PORT, HOST
from src.db import Db
from src.db_schema import TABLE_NAMES, STATUSES_TABLE, USERS_TABLE, TASKS_TABLE


class Seeder(Db):
    def __init__(self, database, user, password, port, host):
        super().__init__(database, user, password, port, host)
        self.faker = Faker('uk_UA')

    def fill_statuses(self):
        for status in ['new', 'in progress', 'completed']:
            self.query("INSERT INTO statuses(name) VALUES(%s)", [status])

    def fill_users(self, count=10):
        for status in range(count):
            self.query("INSERT INTO users(fullname, email ) VALUES(%s, %s)",
                       [self.faker.full_name(), self.faker.email()])

    def fill_tasks(self, count=100, user_count=10):
        for status in range(count):
            self.query("INSERT INTO tasks(title, description, status_id, user_id) VALUES(%s, %s, %s, %s)",
                       [
                           self.faker.sentence(nb_words=5),
                           ' '.join(self.faker.sentences(nb=10)),
                           random.choice([None, 1, 2, 3]),
                           random.choice([None] + list(range(3, user_count + 1)))
                       ])
            self.query("""UPDATE tasks SET description=NULL WHERE id IN (2,5,6) """)

    def fill_database(self):
        self.fill_statuses()
        self.fill_users()
        self.fill_tasks()


if __name__ == '__main__':

    seeder = Seeder(DATABASE, USER, PASSWORD, PORT, HOST)

    for table_query in [STATUSES_TABLE, USERS_TABLE, TASKS_TABLE]:
        seeder.query(table_query)

    seeder.fill_database()

