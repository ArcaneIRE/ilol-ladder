import csv
from player import Player
from output import buildPage
from functools import cmp_to_key

if __name__ == "__main__":
    players = []
    with open('app/players.csv', newline='', encoding="utf-8") as players_file:
        reader = csv.reader(players_file)
        for row in reader:
            name = row[0]
            role = row[1]
            puuids = list(row[2:])
            player = Player(name, role, puuids)

            if player.highest_rank_summoner:
                players.append(player)

    def cmp_func(x, y):
        return x.compare_rank_to(y)

    sorted_players = sorted(players, key=cmp_to_key(cmp_func), reverse=True)
    buildPage(sorted_players)
