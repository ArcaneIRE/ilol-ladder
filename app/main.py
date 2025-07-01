import argparse
import csv
import logging
from player import Player
from output import build_page
from functools import cmp_to_key

def setup_logging(debug=False):
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s|%(levelname)s|%(module)s|%(message)s')
    logger = logging.getLogger(__name__)
    return logger

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ilol Ladder application')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()

    logger = setup_logging(args.debug)

    logger.info("Running...")
    if args.debug:
        logger.debug("Debug mode enabled")

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
    build_page(sorted_players)
    logger.info("Page built successfully")
