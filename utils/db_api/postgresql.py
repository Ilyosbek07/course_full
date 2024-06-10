from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        language VARCHAR(255) NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, telegram_id, username):
        sql = "INSERT INTO app_tguser (full_name, telegram_id,username) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, telegram_id, username, fetchrow=True)

    async def add_user_with_competition_refer_id(self, full_name, telegram_id, username, competition_refer_id):
        sql = "INSERT INTO app_tguser (full_name, telegram_id,username,competition_refer_id) VALUES($1, $2, $3,$4) returning *"
        return await self.execute(sql, full_name, telegram_id, username, competition_refer_id, fetchrow=True)

    async def select_all_competition_refer_id(self, competition_refer_id):
        sql = "SELECT * FROM app_tguser WHERE competition_refer_id=$1"
        return await self.execute(sql, competition_refer_id, fetch=True)

    async def select_user(self, telegram_id):
        sql = "SELECT * FROM app_tguser WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM app_tguser"
        return await self.execute(sql, fetchval=True)

    async def update_user_score(self, score, telegram_id):
        sql = "UPDATE app_tguser SET score=$1 WHERE telegram_id=$2"
        return await self.execute(sql, score, telegram_id, execute=True)

    async def update_user_name(self, full_name, telegram_id):
        sql = "UPDATE app_tguser SET full_name=$1 WHERE telegram_id=$2"
        return await self.execute(sql, full_name, telegram_id, execute=True)

    async def update_user_card(self, card, telegram_id):
        sql = "UPDATE app_tguser SET card=$1 WHERE telegram_id=$2"
        return await self.execute(sql, card, telegram_id, execute=True)

    async def update_user_phone(self, phone, telegram_id):
        sql = "UPDATE app_tguser SET phone=$1 WHERE telegram_id=$2"
        return await self.execute(sql, phone, telegram_id, execute=True)

    async def update_user_data(self, full_name, phone, card, telegram_id):
        sql = "UPDATE app_tguser SET full_name=$1,phone=$2,card=$3 WHERE telegram_id=$4"
        return await self.execute(sql, full_name, phone, card, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM app_tguser WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE app_tguser", execute=True)

    async def select_all_offerta(self):
        sql = "SELECT * FROM app_offerta"
        return await self.execute(sql, fetch=True)

    # course
    async def select_course_by_title(self, title):
        sql = "SELECT * FROM app_course WHERE title=$1"
        return await self.execute(sql, title, fetchrow=True)

    async def select_all_courses(self):
        sql = "SELECT * FROM app_course"
        return await self.execute(sql, fetch=True)

    async def update_course_file_id(self, file_id, course_id):
        sql = "UPDATE app_course SET file_id=$1 WHERE id=$2"
        return await self.execute(sql, file_id, course_id, execute=True)
