from db_conn import get_db_connection


def create_db():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Таблица пользователей
            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY, 
                user_id BIGSERIAL UNIQUE NOT NULL,
            )
            """
            )

            # Таблица избранных пользователей
            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS chosen_people (
                id SERIAL PRIMARY KEY,
                user_id BIGSERIAL,
                name_and_surname_human VARCHAR(100),
                link_profile VARCHAR(155),
                photo VARCHAR(255),
                FOREIGN KEY(user_id) REFERENCES users(user_id),
            )
            """
            )

            # Таблица черного списка
            cur.execute(
                """
            CREATE TABLE IF NOT EXISTS dark_list (
                id SERIAL PRIMARY KEY,
                user_id BIGSERIAL,
                user_id_dark BIGSERIAL,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
            """
            )


# Добавление пользователя
def ensure_user_exists(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            INSERT INTO users (user_id)
            VALUES (%s)
            ON CONFLICT (user_id) DO NOTHING
            """,
                (user_id),
            )

            conn.commit()


# Добавление изранных пользователей
def adding_favorite_users(user_id, name_and_surname_human, link_profile, photo):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            INSERT INTO chosen_people (user_id, name_and_surname_human, link_profile, photo)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id, name_and_surname_human) DO NOTHING
            """,
                (user_id, name_and_surname_human, link_profile, photo),
            )


# Добавление в чс
def adding_dark_list(user_id, user_id_dark):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            INSERT INTO derk_list (user_id, user_id_dark)
            VALUES (%s, %s)
            ON CONFLICT (user_id, user_id_dark) DO NOTHING
            """,
                (user_id, user_id_dark),
            )


# Выод избранных пользователей
def display_of_favorite_users(user_id):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            SELECT name_and_surname_human, link_profile, photo FROM chosen_people
            WHERE user_id = %s
            """,
                (user_id,),
            )
