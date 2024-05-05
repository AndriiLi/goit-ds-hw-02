from colorama import Fore

from src.config import DATABASE, USER, PASSWORD, PORT, HOST
from src.db_schema import STATUS_PROGRESS, STATUS_NEW, STATUS_COMPLETE
from src.queries import Query


def print_colored(message: str) -> None:
    color = Fore.BLUE
    print(f"{color}{message}{Fore.RESET}")


def main():
    print_colored("Hello let`s test some query together :)")

    query = Query(DATABASE, USER, PASSWORD, PORT, HOST)

    while True:
        try:
            print(
                """
                1.Отримати всі завдання певного користувача. Використайте SELECT для отримання завдань конкретного користувача за його user_id.
                2.Вибрати завдання за певним статусом. Використайте підзапит для вибору завдань з конкретним статусом, наприклад, 'new'.
                3.Оновити статус конкретного завдання. Змініть статус конкретного завдання на 'in progress' або інший статус.
                4.Отримати список користувачів, які не мають жодного завдання. Використайте комбінацію SELECT, WHERE NOT IN і підзапит.
                5.Додати нове завдання для конкретного користувача. Використайте INSERT для додавання нового завдання.
                6.Отримати всі завдання, які ще не завершено. Виберіть завдання, чий статус не є 'завершено'.
                7.Видалити конкретне завдання. Використайте DELETE для видалення завдання за його id.
                8.Знайти користувачів з певною електронною поштою. Використайте SELECT із умовою LIKE для фільтрації за електронною поштою.
                9.Оновити ім'я користувача. Змініть ім'я користувача за допомогою UPDATE.
                10.Отримати кількість завдань для кожного статусу. Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами.
                11.Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти. Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені користувачам, чия електронна пошта містить певний домен (наприклад, '%@example.com').
                12.Отримати список завдань, що не мають опису. Виберіть завдання, у яких відсутній опис.
                13.Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом.
                14.Отримати користувачів та кількість їхніх завдань. Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.
                """
            )

            command = str(input("Choose number query:"))
            match command:
                case "close" | "exit" | "q" | "quit":
                    print_colored("Good bye!")
                    break
                case "1":
                    user_id = 9
                    result = query.get_all_user_tasks(user_id)
                    print_colored(f"Tasks for  user with id: {user_id} count: {len(result)} \n {result}")
                case "2":
                    status = STATUS_NEW['name']
                    result = query.get_all_tasks_with_by_status(status)
                    print_colored(f"all tasks with {status} status, count:{len(result)}   \n {result}")
                case "3":
                    task_id = 12
                    status_id = STATUS_PROGRESS['key']
                    updated_task_id = query.update_some_tas_status(task_id, status_id)
                    print_colored(f"task id {updated_task_id} update status id to {status_id} ")
                case "4":
                    result = query.get_users_without_tasks()
                    print_colored(f" users which no any tasks, count: {len(result)}  \n {result}")
                case "5":
                    task = [
                        query.faker.sentence(nb_words=5),
                        ' '.join(query.faker.sentences(nb=5)),
                        STATUS_NEW['key'],
                        9
                    ]
                    new_task_id = query.insert_new_tasks(task)
                    print_colored(f"Created new task \n {new_task_id}")
                case "6":
                    not_complete = query.get_all_not_competed_tasks(STATUS_COMPLETE['key'])
                    print_colored(f"All not completed tasks count: {len(not_complete)} \n {not_complete}")
                case "7":
                    task_id = 1
                    print_colored(f"Task id {task_id} has been deleted  {query.delete_task_by_id(task_id)}")
                case "8":
                    email_template = 'example.net'
                    result = query.get_user_by_email_template(email_template)
                    print_colored(f"Users with email *@{email_template} count: {len(result)} \n {result}")
                case "9":
                    user_id = 2
                    new_full_name = query.faker.full_name()
                    updated_user_id = query.update_user_fullname_by_id(user_id, new_full_name)
                    print_colored(f"User {updated_user_id} updated new fullname {new_full_name}")
                case "10":
                    print_colored(f"Count tasks by statuses \n {query.get_count_tasks_by_statuses()}")
                case "11":
                    email_template = 'example.net'
                    result = query.get_tasks_user_by_email_template(email_template)
                    print_colored(f"Tasks by email template count: {len(result)} \n {result}")
                case "12":
                    result = query.get_tasks_without_description()
                    print_colored(f"Tasks without description count: {len(result)} \n {result}")
                case "13":
                    result = query.get_users_tasks_in_progress_statuses()
                    print_colored(f"Users and tasks in progress status count: {len(result)} \n {result}")
                case "14":
                    print_colored(f"Users with count tasks \n {query.get_users_wth_count_tasks()}")
                case _:
                    print('unknown input')

        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
