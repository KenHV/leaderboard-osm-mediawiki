import asyncio
import xml.etree.ElementTree as ET

import aiohttp


def calculate_total_score(xml: str, skip_last: bool = False) -> int:
    root = ET.fromstring(xml)
    total_score = 0
    if skip_last:
        root = root[:-1]
    for changeset in root:
        score = int(changeset.attrib.get("changes_count"))  # type: ignore
        total_score += score
    return total_score


async def get_changeset(user: str, time: str = None) -> str:
    url = "https://api.openstreetmap.org/api/0.6/changesets"
    params = {"display_name": user}  # "time": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    if time:
        params["time"] = time
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            xml = await response.text()
    return xml


async def main():
    user = input("Enter username: ")
    time = input("Enter time in %Y-%m-%dT%H:%M:%SZ format (optional): ")

    if time:
        xml = await get_changeset(user, time)
    else:
        xml = await get_changeset(user)

    score = calculate_total_score(xml)

    print(f"User: {user} | Score: {score}")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
