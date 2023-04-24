import csv
from player import Player
from output import buildPage
from functools import cmp_to_key

from dotenv import load_dotenv
import os
from riotwatcher import LolWatcher, ApiError
from rank import Rank

load_dotenv()
api_token = os.environ.get("API_KEY")
lol_watcher = LolWatcher(api_token)
region = 'EUW1'


def get_puuids(usernames):
    puuids = []
    for username in usernames:
        account_info = lol_watcher.summoner.by_name(region, username)
        puuids.append(account_info['puuid'])
    return puuids


if __name__ == "__main__":
    players = []
    with open('api-app\players.csv', newline='', encoding="utf-8") as players_file:
        reader = csv.reader(players_file)
        for row in reader:
            name = row[0]
            role = row[1]
            usernames = list(row[2:])
            puuids = get_puuids(usernames)
            player = [name, role]
            player.extend(puuids)
            players.append(player)

    with open('api-app\players_puuids.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        for player in players:
            writer.writerow(player)
