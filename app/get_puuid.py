from dotenv import load_dotenv
import os
import csv
import logging
from riotwatcher import LolWatcher, ApiError

load_dotenv()
api_token = os.environ.get("API_KEY")
lol_watcher = LolWatcher(api_token)
region = 'EUW1'

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    usernames = []
    finished = False
    while not finished:
        username = input("Enter a username (type 'done' if finished): ")
        if username == "done":
            if len(usernames) > 0:
                finished = True
            else:
                print("No username has been entered yet")
        else:
            print("Added.")
            usernames.append(username)
            logger.info(f"Username added: {username}")

    puuids = []
    for username in usernames:
        try:
            response = lol_watcher.summoner.by_name(region, username)
            puuids.append(response['puuid'])
            logger.info(f"PUUID fetched for {username}: {response['puuid']}")
        except ApiError as e:
            logger.error(f"Error fetching PUUID for {username}: {e}")

    logger.debug(f"Usernames: {usernames}")
    logger.debug(f"PUUIDs: {puuids}")
    print(usernames, "\n", puuids)
