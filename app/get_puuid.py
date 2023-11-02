from dotenv import load_dotenv
import os
import csv
from riotwatcher import LolWatcher, ApiError

load_dotenv()
api_token = os.environ.get("API_KEY")
lol_watcher = LolWatcher(api_token)
region = 'EUW1'

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

    puuids = []
    for username in usernames:
        response = lol_watcher.summoner.by_name(region, username)
        puuids.append(response['puuid'])

    print(usernames, "\n", puuids)
