import asyncio

import aiohttp


async def get_response(user: str) -> str:
    url = "https://www.mediawiki.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "users",
        "ususers": user,
        "usprop": "editcount",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            json = await response.json()
    return json


def calculate_score(json: str) -> int:
    return int(json["query"]["users"][0]["editcount"])  # type: ignore


async def mw_get_score(user: str) -> int:
    response = await get_response(user)
    score = calculate_score(response)
    return score


async def main():
    user = input("Enter username: ")
    response = await get_response(user)
    try:
        score = calculate_score(response)
    except Exception:
        print("Couldn't fetch score.")
        return

    print(f"User: {user} | Score: {score}")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
