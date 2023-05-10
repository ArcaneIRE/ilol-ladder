from dotenv import load_dotenv
import os
from riotwatcher import LolWatcher, ApiError
from rank import Rank
from summoner import Summoner

load_dotenv()
api_token = os.environ.get("API_KEY")
lol_watcher = LolWatcher(api_token)
region = 'EUW1'


class Player:
    def __init__(self, name, role, puuids):
        self.name = name
        self.role = role
        self.summoners = []
        for puuid in puuids:
            self.summoners.append(Summoner(puuid))
        self.highest_rank_summoner = self.__get_highest_rank_summoner()

    def __get_highest_rank_summoner(self):
        highest = None
        for current in self.summoners:
            if current.rank:
                if highest == None:
                    highest = current
                elif current.rank > highest.rank:
                    highest = current
        return highest

    def compare_rank_to(self, other_player):
        if other_player.__class__ is not self.__class__:
            return NotImplemented
        my_rank = self.highest_rank_summoner.rank
        their_rank = other_player.highest_rank_summoner.rank
        if my_rank > their_rank:
            return 1
        elif my_rank == their_rank:
            return 0
        else:
            return -1
