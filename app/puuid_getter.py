import csv
import logging
from player import Player
from output import buildPage
from functools import cmp_to_key

from dotenv import load_dotenv
import os
from riotwatcher import LolWatcher, ApiError
from rank import Rank

load_dotenv()
API_TOKEN = os.environ.get("API_KEY")
LOL_WATCHER = LolWatcher(API_TOKEN)
REGION = 'EUW1'

logger = logging.getLogger(__name__)

def get_puuids(usernames):
    logger.info(f"Fetching PUUIDs for usernames: {usernames}")
    puuids = []
    for username in usernames:
        account_info = LOL_WATCHER.summoner.by_name(REGION, username)
        puuids.append(account_info['puuid'])
    logger.info(f"PUUIDs fetched: {puuids}")
    return puuids

if __name__ == "__main__":
    logger.info("Running PUUID getter script...")
    players = []
    try:
        with open('app/players.csv', newline='', encoding="utf-16") as players_file:
            reader = csv.reader(players_file)
            for row in reader:
                name = row[0]
                role = row[1]
                usernames = list(row[2:])
                puuids = get_puuids(usernames)
                player = [name, role]
                player.extend(puuids)
                players.append(player)
    except Exception as e:
        logger.error(f"Error reading players file: {e}")

    try:
        with open('app/players_puuids.csv', 'w', newline='', encoding="utf-16") as f:
            writer = csv.writer(f)
            for player in players:
                writer.writerow(player)
        logger.info("PUUIDs written to app/players_puuids.csv")
    except Exception as e:
        logger.error(f"Error writing PUUIDs to file: {e}")
