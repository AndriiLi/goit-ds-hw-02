from faker import Faker
from src.db import Db


class Query(Db):
    def __init__(self, database, user, password, port, host):
        super().__init__(database, user, password, port, host)
        self.faker = Faker('uk_UA')

    def get_all_user_tasks(self, user_id):
        """
             Отримати всі завдання певного користувача.
             Використайте SELECT для отримання завдань конкретного користувача за його user_id.
        """
        return self.fetch_all(
            """
            SELECT *
            FROM tasks
            WHERE user_id = %s
            ORDER BY id;
            """,
            [user_id]
        )

    def get_all_tasks_with_by_status(self, status):
        """
        Вибрати завдання за певним статусом.
        Використайте підзапит для вибору завдань з конкретним статусом, наприклад, 'new'.
        """
        return self.fetch_all(
            """
             SELECT *
             FROM tasks
             WHERE status_id  = (
                SELECT id
                FROM statuses
                WHERE name = %s
                )
             ORDER BY id;""",
            [status]
        )

    def update_some_tas_status(self, task_id=10, status_id=2) -> int:
        """
            Оновити статус конкретного завдання. Змініть статус конкретного завдання на 'in progress' або інший статус.
        """
        return self.fetch_one("UPDATE tasks SET status_id = %s WHERE id = %s RETURNING id", [status_id, task_id])

    def get_users_without_tasks(self) -> list:
        """
            Отримати список користувачів, які не мають жодного завдання.
            Використайте комбінацію SELECT, WHERE NOT IN і підзапит.
        """

        return self.fetch_all(
            """
            SELECT *
            FROM users
            WHERE id NOT IN (
                SELECT DISTINCT user_id
                FROM tasks
                WHERE user_id IS NOT NULL
            )
            """
        )

    def insert_new_tasks(self, task) -> int:
        """
        Додати нове завдання для конкретного користувача.
        Використайте INSERT для додавання нового завдання.
        """
        return self.fetch_one(
            """
            INSERT INTO tasks(title, description, status_id, user_id) VALUES (%s, %s, %s, %s) RETURNING id;
            """,
            task
        )

    def get_all_not_competed_tasks(self, status_id: int) -> list:
        """
        Отримати всі завдання, які ще не завершено.
        Виберіть завдання, чий статус не є 'завершено'.
        """
        return self.fetch_all(
            """SELECT *
               FROM tasks
               WHERE status_id != %s
               ORDER by id;
             """, [status_id]
        )

    def delete_task_by_id(self, task_id: int) -> int:
        """
        Видалити конкретне завдання.
        Використайте DELETE для видалення завдання за його id.
        """
        return self.fetch_one("DELETE FROM tasks WHERE id = %s RETURNING id;", [task_id])

    def get_user_by_email_template(self, template: str = 'example.org'):
        """
        Знайти користувачів з певною електронною поштою.
        Використайте SELECT із умовою LIKE для фільтрації за електронною поштою.
        """
        return self.fetch_all(
            """ SELECT fullname, email FROM users WHERE email LIKE %s """, [f"%@{template}"]
        )

    def update_user_fullname_by_id(self, user_id: int, fullname: str) -> int:
        """
        Оновити ім'я користувача.
        Змініть ім'я користувача за допомогою UPDATE.
        """
        return self.fetch_one(
            """ UPDATE users SET fullname = %s WHERE id = %s RETURNING id""",
            [fullname, user_id]
        )

    def get_count_tasks_by_statuses(self) -> list:
        """
        Отримати кількість завдань для кожного статусу.
        Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами.
        """
        return self.fetch_all(
            """
            SELECT s.id, s.name, x.cnt
            FROM statuses AS s
            INNER JOIN (
                SELECT status_id, COUNT(id) AS cnt
                FROM tasks AS t
                GROUP BY status_id
            ) AS x ON x.status_id = s.id
            """
        )

    def get_tasks_user_by_email_template(self, template: str = 'example.org') -> list:
        """
        Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
        Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені користувачам,
        чия електронна пошта містить певний домен (наприклад, '%@example.com').
        """
        return self.fetch_all(
            """
            SELECT t.user_id,u.email, u.fullname, t.id AS task_id, t.title, s.name  FROM tasks AS t
            INNER JOIN users AS u ON u.id = t.user_id
            LEFT JOIN statuses AS s ON s.id = t.status_id
            WHERE u.email LIKE %s
            """,
            [f"%@{template}"]
        )

    def get_tasks_without_description(self) -> list:
        """
        Отримати список завдань, що не мають опису.
        Виберіть завдання, у яких відсутній опис.
        """
        return self.fetch_all(
            """
            SELECT t.id, t.title, t.description FROM tasks AS t
            WHERE t.description IS NULL
            """
        )

    def get_users_tasks_in_progress_statuses(self) -> list:
        """
        Вибрати користувачів та їхні завдання, які є у статусі 'in progress'.
        Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом.
        """
        return self.fetch_all(
            """
            SELECT u.id, u.fullname, t.id AS task_id,  t.title, s.name
            FROM tasks AS t
            INNER JOIN statuses AS s ON s.id = t.status_id
            INNER JOIN users AS u ON u.id = t.user_id
            WHERE s.name  = 'in progress'
            ORDER BY u.id
            """
        )

    def get_users_wth_count_tasks(self) -> list:
        """
        Отримати користувачів та кількість їхніх завдань.
        Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.
        """
        return self.fetch_all(
            """
            SELECT u.id, u.fullname, COALESCE(x.count_tasks, 0),
            CASE
                WHEN x.count_tasks is NULL THEN 'no tasks'
                ELSE 'has task'
              END  AS status
            FROM users AS u
            LEFT JOIN (
                SELECT t.user_id, COUNT(t.user_id) AS count_tasks
                FROM tasks AS t 
                GROUP BY t.user_id
            ) AS x ON x.user_id = u.id
            ORDER BY status DESC 
            """
        )

    def get_task_by_id(self, task_id: int) -> list:
        return self.fetch_all(
            """
            SELECT * from tasks WHERE id = %s
            """,
            [task_id]
        )
