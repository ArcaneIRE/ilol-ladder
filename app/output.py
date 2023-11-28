from bs4 import BeautifulSoup
from datetime import datetime


with open('docs/index.html', 'r+', encoding="utf-16") as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'html.parser')


def buildPage(players):
    add_players(players)
    add_timestamp()
    with open('docs/index.html', 'w', encoding="utf-16") as f:
        f.write(str(soup.prettify()))


def add_players(players):
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


def build_opgg(player):
    if len(player.summoners) == 1:
        return "https://www.op.gg/summoners/euw/" + player.summoners[0].riot_id
    else:
        riot_ids = []
        for summoner in player.summoners:
            riot_ids.append(summoner.riot_id)
        return "https://www.op.gg/multisearch/euw?summoners=" + \
            ','.join(riot_ids)


def add_timestamp():
    timestamp = soup.find("div", class_='timestamp')
    timestamp.clear()
    current_time = datetime.now().strftime("%H:%M")
    current_date = datetime.now().strftime("%d/%m/%Y")
    time_string = "Last Refresh: " + \
        current_time + " (Irish time) " + current_date
    timestamp.append(time_string)
