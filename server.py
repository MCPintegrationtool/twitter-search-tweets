# Based on example from https://github.com/xdevplatform/Twitter-API-v2-sample-code/blob/main/Recent-Search/recent_search.py
import requests
import os
import json
from fastmcp import FastMCP

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")
if not bearer_token:
    raise EnvironmentError("BEARER_TOKEN environment variable not set")

search_url = "https://api.twitter.com/2/tweets/search/recent"

# Create a basic server instance
mcp = FastMCP(name="TwitterMCPServer")

def connect_to_endpoint(url, params):
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2RecentSearchPython"
    }
    response = requests.get(url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

@mcp.tool(name="search recent tweets", description="Search recent tweets")
def search_recent_tweets(query_params: str) -> str:
    """
    Search recent tweets using the Twitter API v2.
    :param query_params: The query string for the search.
    :return: JSON string of the response.
    """
    query = {'query': f"{query_params}"}
    json_response = connect_to_endpoint(search_url, query)
    return "json.dumps(json_response, indent=4, sort_keys=True)"

if __name__ == "__main__":
    # This runs the server, defaulting to STDIO transport
    mcp.run()
