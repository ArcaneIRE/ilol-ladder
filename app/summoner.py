from dotenv import load_dotenv
import os
import logging
from riotwatcher import LolWatcher, RiotWatcher, ApiError
from rank import Rank

load_dotenv()
API_TOKEN = os.environ.get("API_KEY")
LOL_WATCHER = LolWatcher(API_TOKEN)
RIOT_WATCHER = RiotWatcher(API_TOKEN)
RIOT_REGION = 'europe'
REGION = 'EUW1'

logger = logging.getLogger(__name__)

class Summoner:
    def __init__(self, puuid):
        logger.info(f"Fetching summoner info for PUUID: {puuid}")
        self.summoner_info = LOL_WATCHER.summoner.by_puuid(REGION, puuid)
        account = RIOT_WATCHER.account.by_puuid(RIOT_REGION, puuid)
        self.riot_id = [account['gameName'],  account['tagLine']]
        self.rank = self.__get_rank()
        logger.info(f"Summoner info fetched for PUUID: {puuid}")

    def __get_rank(self):
        summoner_id = self.summoner_info['id']
        all_queue_stats = LOL_WATCHER.league.by_summoner(REGION, summoner_id)
        if not all_queue_stats:
            return

        for queue_stats in all_queue_stats:
            if queue_stats['queueType'] == "RANKED_SOLO_5x5":
                tier = queue_stats['tier']
                division = queue_stats['rank']
                lp = queue_stats['leaguePoints']
                return Rank(tier, division, lp)
