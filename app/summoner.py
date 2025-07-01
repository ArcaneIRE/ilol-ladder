from dotenv import load_dotenv
import os
import logging
import time
from riotwatcher import LolWatcher, RiotWatcher, ApiError
from rank import Rank

load_dotenv()
API_TOKEN = os.environ.get("API_KEY")
LOL_WATCHER = LolWatcher(API_TOKEN)
RIOT_WATCHER = RiotWatcher(API_TOKEN)
RIOT_REGION = 'europe'
REGION = 'EUW1'

logger = logging.getLogger(__name__)

def execute_with_retry(api_function, max_retries=5, initial_backoff=30):
    """Execute an API call with retry logic for rate limiting"""
    retries = 0
    backoff = initial_backoff
    
    while True:
        try:
            return api_function()
        except ApiError as e:
            if e.response.status_code == 429:  # Rate limit error
                retry_after = e.response.headers.get('Retry-After', backoff)
                try:
                    retry_after = int(retry_after)
                except (ValueError, TypeError):
                    retry_after = backoff
                
                retries += 1
                if retries > max_retries:
                    logger.error(f"Maximum retries ({max_retries}) exceeded for API call")
                    raise
                
                logger.warning(f"Rate limit hit. Waiting for {retry_after} seconds before retry {retries}/{max_retries}")
                time.sleep(retry_after)
                backoff = min(backoff * 2, 120)  # Exponential backoff, capped at 2 minutes
            else:
                raise

class Summoner:
    def __init__(self, puuid):
        logger.info(f"Fetching summoner info for PUUID: {puuid}")
        account = execute_with_retry(lambda: RIOT_WATCHER.account.by_puuid(RIOT_REGION, puuid))
        self.riot_id = [account['gameName'],  account['tagLine']]
        self.rank = self.__get_rank(puuid)
        logger.info(f"Summoner info fetched for PUUID: {puuid}")

    def __get_rank(self, puuid):
        all_queue_stats = execute_with_retry(lambda: LOL_WATCHER.league.by_puuid(REGION, puuid))
        if not all_queue_stats:
            return

        for queue_stats in all_queue_stats:
            if queue_stats['queueType'] == "RANKED_SOLO_5x5":
                tier = queue_stats['tier']
                division = queue_stats['rank']
                lp = queue_stats['leaguePoints']
                return Rank(tier, division, lp)
