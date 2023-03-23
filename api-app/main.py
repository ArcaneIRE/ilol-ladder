import csv
from player import Player
from output import buildPage
from functools import cmp_to_key

if __name__ == "__main__":
    players = []
    with open('api-app/players.csv', newline='', encoding="utf-8") as players_file:
        reader = csv.reader(players_file)
        for row in reader:
            name = row[0]
            role = row[1]
            usernames = list(row[2:])
            player = Player(name, role, usernames)

            if player.rank:
                players.append(player)

    def cmp_func(x, y):
        return x.compare_rank(y)

    sorted_players = sorted(players, key=cmp_to_key(cmp_func), reverse=True)
    buildPage(sorted_players)
