from bs4 import BeautifulSoup
from datetime import datetime


with open('docs\index.html', 'r+') as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'html.parser')


def buildPage(players):
    add_players(players)
    add_timestamp()
    with open('docs\index.html', 'w') as f:
        f.write(str(soup.prettify()))


def add_players(players):
    ladder = soup.find("ol", class_='ladder')
    ladder.clear()
    for player in players:
        player_tag = soup.new_tag('li')
        player_tag.string = player.name + ": " + str(player.rank)
        ladder.append(player_tag)


def add_timestamp():
    timestamp = soup.find("div", class_='timestamp')
    timestamp.clear()
    current_time = datetime.now().strftime("%H:%M %d/%m/%Y")
    time_string = "Last Refreshed: " + current_time + "(Irish time)"
    timestamp.append(time_string)
