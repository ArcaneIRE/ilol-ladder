from bs4 import BeautifulSoup


def buildPage(players):
    with open('docs\index.html', 'r+') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')

    ladder = soup.find("ol", class_='ladder')
    ladder.clear()
    for player in players:
        player_tag = soup.new_tag('li')
        player_tag.string = player.name + ": " + str(player.rank)
        ladder.append(player_tag)

    with open('docs\index.html', 'w') as f:
        f.write(str(soup.prettify()))
