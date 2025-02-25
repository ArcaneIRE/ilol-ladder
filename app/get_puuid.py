from dotenv import load_dotenv
import os
import logging
from riotwatcher import LolWatcher, ApiError

load_dotenv()
API_TOKEN = os.environ.get("API_KEY")
LOL_WATCHER = LolWatcher(API_TOKEN)
REGION = 'EUW1'

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
            response = LOL_WATCHER.summoner.by_name(REGION, username)
            puuids.append(response['puuid'])
            logger.info(f"PUUID fetched for {username}: {response['puuid']}")
        except ApiError as e:
            logger.error(f"Error fetching PUUID for {username}: {e}")

    logger.debug(f"Usernames: {usernames}")
    logger.debug(f"PUUIDs: {puuids}")
    print(usernames, "\n", puuids)
