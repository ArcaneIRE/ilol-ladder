from bs4 import BeautifulSoup
from datetime import datetime


with open('docs/index.html', 'r+') as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'html.parser')


def buildPage(players):
    add_players(players)
    add_timestamp()
    with open('docs/index.html', 'w', encoding="utf-8") as f:
        f.write(str(soup.prettify()))


def add_players(players):
    ladder = soup.find("ol", class_='ladder')
    ladder.clear()
    for player in players:
        tag = soup.new_tag('li')

        name = soup.new_tag('a')
        name.string = player.name
        name['class'] = "name"
        name['href'] = get_opgg(player)
        tag.append(name)

        rank = soup.new_tag('span')
        rank.string = str(player.rank)
        rank['class'] = "rank " + player.rank.tier.name.lower()
        tag.append(rank)

        ladder.append(tag)


def get_opgg(player):
    if len(player.usernames) > 1:
        return "https://www.op.gg/multisearch/euw?summoners=" + \
            ','.join(player.usernames)
    else:
        return "https://www.op.gg/summoners/euw/" + player.usernames[0]


def add_timestamp():
    timestamp = soup.find("div", class_='timestamp')
    timestamp.clear()
    current_time = datetime.now().strftime("%H:%M")
    current_date = datetime.now().strftime("%d/%m/%Y")
    time_string = "Last Refresh: " + \
        current_time + " (Irish time) " + current_date
    timestamp.append(time_string)
