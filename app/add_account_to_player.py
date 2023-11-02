from dotenv import load_dotenv
import os
import csv
from riotwatcher import LolWatcher, ApiError

from tempfile import NamedTemporaryFile
import shutil

load_dotenv()
api_token = os.environ.get("API_KEY")
lol_watcher = LolWatcher(api_token)
region = 'EUW1'

if __name__ == "__main__":
    name = input("Enter their player name: ")

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

    temp_file = NamedTemporaryFile(
        mode='w', newline='', delete=False, encoding="utf-16")
    with open('app/players.csv', 'r', newline='', encoding="utf-16") as players_file, temp_file:
        reader = csv.reader(players_file)
        writer = csv.writer(temp_file)

        for row in reader:
            if row[0] == name:
                writer.writerow(row + puuids)
            else:
                writer.writerow(row)
    shutil.move(temp_file.name, 'app/players.csv')
