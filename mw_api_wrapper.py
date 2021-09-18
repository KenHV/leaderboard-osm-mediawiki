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


async def main():
    user = input("Enter username: ")
    json = await get_response(user)
    try:
        score = json["query"]["users"][0]["editcount"]  # type: ignore
    except Exception:
        print("Couldn't fetch score.")
        return

    print(f"User: {user} | Score: {score}")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
