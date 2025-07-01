from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo
import logging

logger = logging.getLogger(__name__)

with open('docs/index.html', 'r+', encoding="utf-16") as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'html.parser')


def build_page(players):
    logger.info("Building page")
    add_players(players)
    add_timestamp()
    with open('docs/index.html', 'w', encoding="utf-16") as f:
        f.write(str(soup.prettify()))
    logger.info("Page written to docs/index.html")


def add_players(players):
    logger.info("Adding players to the page")
    ladder = soup.find("ol", class_='ladder')
    ladder.clear()
    for player in players:
        tag = soup.new_tag('li')

        name = soup.new_tag('a')
        name.string = player.name
        name['class'] = "name"
        name['href'] = build_opgg(player)
        tag.append(name)

        rank = soup.new_tag('span')
        rank.string = str(player.highest_rank_summoner.rank)
        tier = player.highest_rank_summoner.rank.tier.name.lower()
        rank['class'] = "rank " + tier
        tag.append(rank)

        ladder.append(tag)
    logger.info("Players added successfully")


def build_opgg(player):
    logger.info(f"Building op.gg link for player {player.name}")
    if len(player.summoners) == 1:
        return "https://www.op.gg/summoners/euw/" + player.summoners[0].riot_id[0] + '-' + player.summoners[0].riot_id[1]
    else:
        riot_ids = []
        for summoner in player.summoners:
            id = summoner.riot_id[0] + "%23" + summoner.riot_id[1]
            riot_ids.append(id)
        return "https://www.op.gg/multisearch/euw?summoners=" + \
            '%2C'.join(riot_ids)


def add_timestamp():
    logger.info("Adding timestamp to the page")
    timestamp = soup.find("div", class_='timestamp')
    timestamp.clear()
    dublin_timezone = ZoneInfo("Europe/Dublin")
    current_time = datetime.now(dublin_timezone).strftime("%H:%M")
    current_date = datetime.now(dublin_timezone).strftime("%d/%m/%Y")
    time_string = "Last Refresh: " + \
        current_time + " (Irish time) " + current_date
    timestamp.append(time_string)
    logger.info("Timestamp added successfully")
