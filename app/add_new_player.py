from dotenv import load_dotenv
import os
import csv
import logging
from riotwatcher import RiotWatcher

load_dotenv()
API_TOKEN = os.environ.get("API_KEY")
RIOT_WATCHER = RiotWatcher(API_TOKEN)
REGION = 'europe'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Running add new player script...")
    name = input("Enter their player name: ")
    finished = False
    while not finished:
        role = input("Enter their main role (top/jungle/mid/adc/support): ")
        if role in ["top", "jungle", "mid", "adc", "support"]:
            finished = True
        else:
            logger.warning("Invalid role entered")
            print("Invalid role")

    riot_ids = []
    finished = False
    while not finished:
        username = input(
            "Enter a username with tagline separated by # (type 'done' if finished): ")
        if username == "done":
            if len(riot_ids) > 0:
                finished = True
            else:
                logger.warning("No username has been entered yet")
                print("No username has been entered yet")
        else:
            riot_ids.append(username.split('#'))
            logger.info(f"Added username: {username}")

    puuids = []
    for riot_id in riot_ids:
        response = RIOT_WATCHER.account.by_riot_id(
            REGION, riot_id[0], riot_id[1])
        puuids.append(response['puuid'])

    try:
        with open('app/players.csv', 'a', encoding="utf-16") as players_file:
            writer = csv.writer(players_file)
            writer.writerow([name, role, *puuids])
        logger.info(f"Player {name} added to app/players.csv")
    except Exception as e:
        logger.error(f"Error writing player to file: {e}")
