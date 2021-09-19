import asyncio
import xml.etree.ElementTree as ET

import aiohttp


async def get_changeset(user: str, time: str = None) -> str:
    url = "https://api.openstreetmap.org/api/0.6/changesets"
    params = {"display_name": user}  # "time": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    if time:
        params["time"] = time
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            xml = await response.text()
    return xml


def calculate_score(xml: str, skip_last: bool = False) -> int:
    root = ET.fromstring(xml)
    total_score = 0
    if skip_last:
        root = root[:-1]
    for changeset in root:
        score = int(changeset.attrib.get("changes_count"))  # type: ignore
        total_score += score
    return total_score


async def osm_get_score(user: str) -> int:
    response = await get_changeset(user)
    score = calculate_score(response)
    return score


async def main():
    user = input("Enter username: ")
    time = input("Enter time in %Y-%m-%dT%H:%M:%SZ format (optional): ")

    if time:
        xml = await get_changeset(user, time)
    else:
        xml = await get_changeset(user)

    try:
        score = calculate_score(xml)
    except Exception:
        print("Couldn't fetch score.")
        return

    print(f"User: {user} | Score: {score}")


if __name__ == "__main__":
    asyncio.run(main())
