from dotenv import load_dotenv
import os
from riotwatcher import LolWatcher, ApiError
from rank import Rank

load_dotenv()
api_token = os.environ.get("API_KEY")
lol_watcher = LolWatcher(api_token)
region = 'EUW1'


class Summoner:
    def __init__(self, puuid):
        self.summoner_info = lol_watcher.summoner.by_puuid(region, puuid)
        self.username = self.summoner_info['name']
        self.rank = self.__get_rank()

    def __get_rank(self):
        summoner_id = self.summoner_info['id']
        all_queue_stats = lol_watcher.league.by_summoner(region, summoner_id)
        if not all_queue_stats:
            return

        for queue_stats in all_queue_stats:
            if queue_stats['queueType'] == "RANKED_SOLO_5x5":
                tier = queue_stats['tier']
                division = queue_stats['rank']
                lp = queue_stats['leaguePoints']
                return Rank(tier, division, lp)
