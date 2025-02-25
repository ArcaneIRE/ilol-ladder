import logging
from summoner import Summoner

logger = logging.getLogger(__name__)

class Player:
    def __init__(self, name, role, puuids):
        self.name = name
        self.role = role
        self.summoners = []
        logger.info(f"Getting summoner info for {name}")
        for puuid in puuids:
            self.summoners.append(Summoner(puuid))
        self.highest_rank_summoner = self.__get_highest_rank_summoner()
        logger.info(f"Highest rank summoner for {name} is {self.highest_rank_summoner}")

    def __get_highest_rank_summoner(self):
        highest = None
        for current in self.summoners:
            if current.rank:
                if highest is None:
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
