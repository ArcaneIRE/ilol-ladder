from dotenv import load_dotenv
import os
import csv
from riotwatcher import RiotWatcher, ApiError

from tempfile import NamedTemporaryFile
import shutil

load_dotenv()
api_token = os.environ.get("API_KEY")
riot_watcher = RiotWatcher(api_token)
region = 'europe'

if __name__ == "__main__":
    name = input("Enter their player name: ")

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
            print("Added.")
            riot_ids.append(username.split('#'))

    puuids = []
    for riot_id in riot_ids:
        response = riot_watcher.account.by_riot_id(
            region, riot_id[0], riot_id[1])
        puuids.append(response['puuid'])

    temp_file = NamedTemporaryFile(
        mode='w', newline='', delete=False, encoding="utf-16")
    with open('app/players.csv', 'r', newline='', encoding="utf-16") as players_file, temp_file:
        reader = csv.reader(players_file)
        writer = csv.writer(temp_file)

        for row in reader:
            if row[0].lower() == name.lower():
                writer.writerow([*row, *puuids])
            else:
                writer.writerow(row)
    shutil.move(temp_file.name, 'app/players.csv')
