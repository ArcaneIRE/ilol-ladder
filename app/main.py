import csv
import logging
from player import Player
from output import buildPage
from functools import cmp_to_key

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Running...")
    players = []
    try:
        with open('app/players.csv', newline='', encoding="utf-16") as players_file:
            reader = csv.reader(players_file)
            for row in reader:
                name = row[0]
                role = row[1]
                puuids = list(row[2:])
                player = Player(name, role, puuids)

                if player.highest_rank_summoner:
                    players.append(player)
    except Exception as e:
        logger.error(f"Error reading players file: {e}")

    def cmp_func(x, y):
        return x.compare_rank_to(y)

    sorted_players = sorted(players, key=cmp_to_key(cmp_func), reverse=True)
    buildPage(sorted_players)
    logger.info("Page built successfully")
