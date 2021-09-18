import aiosqlite
import asyncio

from mw_api_wrapper import mw_get_score
from osm_api_wrapper import osm_get_score


async def osm_update_scoreboard(db: aiosqlite.Connection) -> None:
    async with db.cursor() as cursor:
        await cursor.execute(
            "SELECT user_email, osm_username, osm_orig_score, osm_current_score FROM leaderboard;"
        )
        users = await cursor.fetchall()

        for user in users:
            # 0: user_email, 1: osm_username, 2: osm_orig_score, 3: osm_current_score
            current_score = await osm_get_score(user[1])
            current_score -= user[2]  # osm_orig_score

            await cursor.execute(
                f"UPDATE leaderboard SET osm_current_score={current_score} WHERE user_email={user[0]}"
            )  # user_email


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


async def main():
    async with aiosqlite.connect("data.sqlite3") as db:
        await osm_update_scoreboard(db)
        await mw_update_scoreboard(db)
        await db.commit()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
