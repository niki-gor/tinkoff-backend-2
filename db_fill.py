import asyncio
import random
from faker import Faker
import asyncpg


USERS_AMOUNT = 1000000
FRIENDS_AMOUNT = 3000000

fake = Faker()
Faker.seed(1234)


async def insert_users(conn):
    users = [
        (
            fake.name(),
            fake.text(),
            random.randint(18, 60),
            fake.email(),
            fake.password(),
            fake.date_time_this_year().strftime("%Y-%m-%d %H:%M:%S"),
        )
        for i in range(USERS_AMOUNT)
    ]
    await conn.executemany(
        "INSERT INTO users (name, about, age, email, hashed_password, last_login_at) VALUES ($1, $2, $3, $4, $5, $6)",
        users,
    )


async def insert_friends(conn):
    friendships = []
    for i in range(FRIENDS_AMOUNT):
        from_id = random.randint(1, USERS_AMOUNT)
        to_id = random.randint(1, USERS_AMOUNT)
        while to_id == from_id:
            to_id = random.randint(1, USERS_AMOUNT)
        accepted_at = (
            str(fake.date_time_between(start_date="-1y", end_date="now", tzinfo=None))
            if random.randint(1, 6) > 2
            else None
        )
        friendships.append((from_id, to_id, accepted_at))
    await conn.executemany(
        "INSERT INTO friends (from_id, to_id, accepted_at) VALUES ($1, $2, $3) ON CONFLICT DO NOTHING",
        friendships,
    )


async def main():
    conn = await asyncpg.connect(
        dsn="postgresql://myuser:mypassword@127.0.0.1:5432/forum"
    )

    await insert_users(conn)
    await insert_friends(conn)

    await conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
