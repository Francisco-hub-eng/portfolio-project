import httpx
import swcpy.swc_config as config
from .schemas import League, Team, Player, Performance
from typing import List
import backoff
import logging
logger = logging.getLogger(__name__)


class SWCClient:

    """ Interacts with the SportsWorldCentral API.
    
    This SDK class simplifies the process of using the SWC Fantasy
    Football API. It supports all the functions of the SWC API and returns
    validated data types.
    
    Typical usage example:
    
        client = SWCClient()
        response = client.get_health_check()
    """

    HEALTH_CHECK_ENDPOINT = "/"
    LIST_LEAGUES_ENDPOINT = "/v0/leagues/"
    LIST_PLAYERS_ENDPOINT = "/v0/players/"
    LIST_PERFORMANCES_ENDPOINT = "/v0/performances/"
    LIST_TEAMS_ENDPOINT = "/v0/teams/"
    GET_COUNTS_ENDPOINT = "/v0/counts/"

    BULK_FILE_BASE_URL = (
        "https://raw.githubusercontent.com/Francisco-hub-eng" + "/portfolio-project/main/bulk"
    )

    def __init__(self, input_config : config.SWCConfig):

        """ Class constructor that sets variables from configuration object."""
        logger.debug(f"Bulk file base URL: {self.BULK_FILE_BASE_URL}")

        logger.debug(f"Input config: {input_config}")

        self.swc_base_url = input_config.swc_base_url
        self.backoff = input_config.swc_backoff
        self.backoff_max_time = input_config.swc_backoff_max_time
        self.bulk_file_format = input_config.swc_bulk_file_format

        self.BULK_FILE_NAMES = {
            "players" : "player_data",
            "leagues" : "league_data",
            "performances" : "performance_data",
            "teams" : "team_data",
            "team_players" : "team_player_data",
        }

        if self.backoff:
            self.get_url = backoff.on_exception(
                Exception(httpx.RequestError, httpx.HTTPStatusError),
                wait_gen = backoff.expo,
                max_time = self.backoff_max_time,
                jitter = backoff.random_jitter,
            )(self.call_api)

        if self.bulk_file_format.lower() == "paquet" :
            self.BULK_FILE_NAMES = {
                key : value + ".paquet" for key, value in self.BULK_FILE_NAMES.items()
            }
        else:
            self.BULK_FILE_NAMES = {
                key : value + ".csv" for key, value in
                self.BULK_FILE_NAMES.items()
            }
        
        logger.debug(f"Bulk file dictionary: {self.BULK_FILE_NAMES}")

    #def get_health_check(self):
    #    # make the API call
    #    with httpx.Client(base_url=self.swc_base_url) as client:
    #        return client.get("/")

        def call_api(
            api_endpoint: str,
            api_params: dict = None       
        ) -> httpx.Response:
            """ Makes API call and logs errors."""

            if api_params:
                api_params = {key: val for key, val in api_params.items() if val is not None}
            try:
                with httpx.Client(base_url=self.swc_base_url) as client:
                    logger.debug(f"base_url: {self.swc_base_url}, api_endpoint: {api_endpoint}, api_params :{api_params}")
                    response = client.get(api_endpoint, params=api_params)
                    logger.debug(f"Response JSON: {response.json()}")
                    return response
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"HTTP statos error ocurred: {e.response.status_code}"
                )
                raise
            except httpx.RequestError as e:
                logger.error(f"Request error occurred: {str(e)}")
                raise