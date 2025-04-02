import psycopg2

from db_conn import get_db_connection

def drop_db():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            DROP TABLE chosen_people;
            DROP TABLE dark_list;
            DROP TABLE users;
            """)

def create_db():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Таблица пользователей
            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY, 
                user_id BIGINT UNIQUE NOT NULL
            )
            """
            )

            # Таблица избранных пользователей
            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS chosen_people (
                id SERIAL PRIMARY KEY,
                user_id BIGINT,
                chosen_user_id BIGINT,
                FOREIGN KEY(user_id) REFERENCES users(user_id),
                UNIQUE (user_id, chosen_user_id)
            )
            """
            )

            # Таблица черного списка
            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS dark_list (
                id SERIAL PRIMARY KEY,
                user_id BIGINT,
                user_id_dark BIGINT,
                FOREIGN KEY(user_id) REFERENCES users(user_id),
                UNIQUE (user_id, user_id_dark)
            )
            """
            )


# Добавление пользователя
def save_user_id(user_id):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                        INSERT INTO users (user_id)
                        VALUES (%s)
                        ON CONFLICT (user_id) DO NOTHING
                    """,
                    (user_id,)
                )
                conn.commit()
    except psycopg2.Error as e:
        print(f"Database error occurred: {e}")
        return None


# Добавление избранных пользователей
def adding_favorite_users(user_id, chosen_user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            INSERT INTO chosen_people (user_id, chosen_user_id)
            VALUES (%s, %s)
            ON CONFLICT (user_id, chosen_user_id) DO NOTHING
            """,
                (user_id, chosen_user_id)
            )


# Добавление в чс
def adding_dark_list(user_id, user_id_dark):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            INSERT INTO dark_list (user_id, user_id_dark)
            VALUES (%s, %s)
            ON CONFLICT (user_id, user_id_dark) DO NOTHING
            """,
                (user_id, user_id_dark,)
            )


# Вывод избранных пользователей
def display_of_favorite_users(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            SELECT chosen_user_id FROM chosen_people
            WHERE user_id = %s
            """,
                (user_id,)
            )
# drop_db()
create_db()
# print(adding_favorite_users(223388613, 826975570))