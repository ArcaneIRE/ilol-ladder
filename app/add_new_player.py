from dotenv import load_dotenv
import os
import csv
from riotwatcher import RiotWatcher, ApiError

load_dotenv()
api_token = os.environ.get("API_KEY")
riot_watcher = RiotWatcher(api_token)
region = 'europe'

if __name__ == "__main__":
    name = input("Enter their player name: ")
    finished = False
    while not finished:
        role = input("Enter their main role (top/jungle/mid/adc/support): ")
        if role in ["top", "jungle", "mid", "adc", "support"]:
            finished = True
        else:
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
                print("No username has been entered yet")
        else:
            riot_ids.append(username.split('#'))
            print("Added.")

    puuids = []
    for riot_id in riot_ids:
        response = riot_watcher.account.by_riot_id(
            region, riot_id[0], riot_id[1])
        puuids.append(response['puuid'])

    with open('app/players.csv', 'a', encoding="utf-16") as players_file:
        writer = csv.writer(players_file)
        writer.writerow([name, role, *puuids])
