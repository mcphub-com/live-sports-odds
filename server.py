import requests
from datetime import datetime
from typing import Union, Literal, List
from mcp.server import FastMCP
from pydantic import Field
from typing import Annotated
from mcp.server.fastmcp import FastMCP
from fastmcp import FastMCP, Context
import os
from dotenv import load_dotenv
load_dotenv()
rapid_api_key = os.getenv("RAPID_API_KEY")

__rapidapi_url__ = 'https://rapidapi.com/theoddsapi/api/live-sports-odds'

mcp = FastMCP('live-sports-odds')

@mcp.tool()
def v4_sports(all: Annotated[Union[bool, None], Field(description='When excluded, only recently updated (in-season) sports appear. Include this paramter to see all available sports')] = None) -> dict: 
    '''Returns a list of available sports and tournaments. Use the `sports_key` in requests for /odds and /scores endpoints.'''
    url = 'https://odds.p.rapidapi.com/v4/sports'
    headers = {'x-rapidapi-host': 'odds.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'all': all,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def sport_odds(regions: Annotated[str, Field(description='Determines which bookmakers appear in the response. Can be a comma delimited list of regions. Each region will count as 1 request against the usage quota for each market. Most use cases will only need to specify one region. For a list of bookmakers by region, see https://the-odds-api.com/sports-odds-data/bookmaker-apis.html')],
               oddsFormat: Annotated[Union[str, None], Field(description='Format of returned odds.')] = None,
               markets: Annotated[Union[str, None], Field(description='The odds market to return. Can be a comma delimited list of odds markets. Defaults to h2h (head to head / moneyline). Outrights only avaialable for select sports. Note each market counts as 1 request against the usage quota.')] = None,
               dateFormat: Annotated[Union[str, None], Field(description='Format of returned timestamps. Can be iso (ISO8601) or unix timestamp (seconds since epoch)')] = None) -> dict: 
    '''Returns list of live and upcoming games for a given sport, showing bookmaker odds for the specified region and markets. Set the `sport` to a `sport_key` from the /sports endpoint. Alternatively if `sport=upcoming`, it will return a list of the next 8 upcoming games across all sports, as well as any live games. For more info, see [list of available sports](https://the-odds-api.com/sports-odds-data/sports-apis.html) and [list of available bookmakers](https://the-odds-api.com/sports-odds-data/bookmaker-apis.html).'''
    url = 'https://odds.p.rapidapi.com/v4/sports/upcoming/odds'
    headers = {'x-rapidapi-host': 'odds.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'regions': regions,
        'oddsFormat': oddsFormat,
        'markets': markets,
        'dateFormat': dateFormat,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def sport_scores(daysFrom: Annotated[Union[int, float, None], Field(description='The number of days in the past from which to return completed games. Valid values are integers from 1 to 3. If this field is missing, only live and upcoming games are returned. Default: 3')] = None) -> dict: 
    '''Returns list of live and upcoming games for a given sport, and optionally recently completed games. Live and completed games will contain scores. **Currently in beta** and only available for selected sports. For more info, see the [list of available sports](https://the-odds-api.com/sports-odds-data/sports-apis.html)'''
    url = 'https://odds.p.rapidapi.com/v4/sports/americanfootball_nfl/scores'
    headers = {'x-rapidapi-host': 'odds.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'daysFrom': daysFrom,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()



if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9997
    mcp.run(transport="stdio")
