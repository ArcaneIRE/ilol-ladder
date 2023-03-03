from dotenv import load_dotenv
import os
from riotwatcher import LolWatcher, ApiError
from rank import Rank

load_dotenv()
api_token = os.environ.get("API_KEY")
lol_watcher = LolWatcher(api_token)
region = 'EUW1'


class Player:
    def __init__(self, name, role, usernames):
        self.name = name
        self.role = role
        self.usernames = usernames
        self.rank = self.__get_highest_rank()

    def __get_rank(self, username):
        summoner_info = lol_watcher.summoner.by_name(region, username)
        summoner_id = summoner_info['id']
        all_queue_stats = lol_watcher.league.by_summoner(region, summoner_id)
        if not all_queue_stats:
            return

        soloq_stats = None
        for queue_stats in all_queue_stats:
            if queue_stats['queueType'] == "RANKED_SOLO_5x5":
                soloq_stats = queue_stats
        tier = soloq_stats['tier']
        division = soloq_stats['rank']
        lp = soloq_stats['leaguePoints']
        return Rank(tier, division, lp)

    def __get_highest_rank(self):
        highest_rank = self.__get_rank(self.usernames[0])
        for username in self.usernames[1:]:
            current_rank = self.__get_rank(username)
            if current_rank:
                if current_rank > highest_rank:
                    highest_rank = current_rank
        return highest_rank

    def compare_rank(self, other_player):
        if self.__class__ is not other_player.__class__:
            return NotImplemented
        if self.rank > other_player.rank:
            return 1
        elif self.rank < other_player.rank:
            return -1
        else:
            return 0
