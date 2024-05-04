STATUSES_TABLE = """
        CREATE TABLE IF NOT EXISTS statuses(
        id SERIAL  PRIMARY KEY NOT NULL,    
        name VARCHAR(50) NOT NULL UNIQUE
        );
"""

USERS_TABLE = """
        CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY NOT NULL,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        updated_at  TIMESTAMP NULL
        );
"""

TASKS_TABLE = """
        CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY NOT NULL,
        title VARCHAR(100) NOT NULL,
        description TEXT NULL,
        status_id INTEGER NULL,
        user_id INTEGER NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP NULL,
        
        FOREIGN KEY (user_id) REFERENCES users(id) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE,
        FOREIGN KEY (status_id) REFERENCES statuses(id) 
            ON DELETE CASCADE 
            ON UPDATE CASCADE
        );
"""


TABLE_NAMES = ['tasks', 'statuses', 'users']

STATUS_NEW = {'key': 1, 'name': 'new'}
STATUS_PROGRESS = {'key': 2, 'name': 'in progress'}
STATUS_COMPLETE = {'key': 3, 'name': 'complete'}

