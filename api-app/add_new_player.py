from dotenv import load_dotenv
import os
import csv
from riotwatcher import LolWatcher, ApiError

load_dotenv()
api_token = os.environ.get("API_KEY")
lol_watcher = LolWatcher(api_token)
region = 'EUW1'

if __name__ == "__main__":
    name = input("Enter their player name: ")
    finished = False
    while not finished:
        role = input("Enter their main role (top/jungle/mid/adc/support): ")
        if role in ["top", "jungle", "mid", "adc", "support"]:
            finished = True
        else:
            print("Invalid role")

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

    puuids = []
    for username in usernames:
        response = lol_watcher.summoner.by_name(region, username)
        puuids.append(response['puuid'])

    with open('api-app/players.csv', 'a', newline='', encoding="utf-8") as players_file:
        writer = csv.writer(players_file)
        writer.writerow([name, role, *puuids])
