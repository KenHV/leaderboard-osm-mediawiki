import asyncio
import os

import aiosqlite

from leaderboard.mainpage.mw_api_wrapper import mw_get_score
from leaderboard.mainpage.osm_api_wrapper import osm_get_score


async def osm_update_scoreboard(db: aiosqlite.Connection) -> None:
    async with db.cursor() as cursor:
        await cursor.execute(
            "SELECT user_email, osm_username, osm_orig_score, osm_current_score FROM leaderboard;"
        )
        users = await cursor.fetchall()

        for user in users:
            # 0: user_email, 1: osm_username, 2: osm_orig_score, 3: osm_current_score
            current_score = await osm_get_score(user[1])  # osm_username
            current_score -= user[2]  # osm_orig_score

            await cursor.execute(
                f"UPDATE leaderboard SET osm_current_score={current_score} WHERE user_email={user[0]}"
            )  # user_email
        await db.commit()


async def mw_update_scoreboard(db: aiosqlite.Connection) -> None:
    async with db.cursor() as cursor:
        await cursor.execute(
            "SELECT user_email, mw_username, mw_orig_score, mw_current_score FROM leaderboard;"
        )
        users = await cursor.fetchall()
        for user in users:
            # 0: user_email, 1: mw_username, 2: mw_orig_score, 3: mw_current_score
            current_score = await mw_get_score(user[1])  # mw_username
            current_score -= user[2]  # mw_orig_score

            await cursor.execute(
                f"UPDATE leaderboard SET mw_current_score={current_score} WHERE user_email={user[0]}"
            )  # user_email
        await db.commit()


async def update_total_score(db: aiosqlite.Connection) -> None:
    async with db.cursor() as cursor:
        await cursor.execute(
            "SELECT user_email, osm_current_score, mw_current_score, total_score FROM leaderboard;"
        )
        users = await cursor.fetchall()
        for user in users:
            # 0: user_email, 1: osm_current_score, 2: mw_current_score, 3: total_score
            total_score = user[1] + user[2]  # osm_current_score + mw_current_score

            await cursor.execute(
                f"UPDATE leaderboard SET total_score={total_score} WHERE user_email={user[0]}"
            )  # user_email
        await db.commit()


async def update_scoreboard(db: aiosqlite.Connection) -> None:
    await osm_update_scoreboard(db)
    await mw_update_scoreboard(db)
    await update_total_score(db)


async def main():
    db_name = "db.sqlite3"
    db_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), db_name)

    async with aiosqlite.connect(db_path) as db:
        await update_scoreboard(db)


if __name__ == "__main__":
    asyncio.run(main())
