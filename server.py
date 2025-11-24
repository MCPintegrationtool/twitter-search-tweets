# Based on example from https://github.com/xdevplatform/Twitter-API-v2-sample-code/blob/main/Recent-Search/recent_search.py
import requests
import os
import json
from fastmcp import FastMCP

# Create a basic server instance
mcp = FastMCP(name="TwitterMCPServer")

@mcp.tool(name="search recent tweets", description="Search recent tweets")
def search_recent_tweets(query_params: str) -> str:
    # To set your environment variables in your terminal run the following line:
    # export 'BEARER_TOKEN'='<your_bearer_token>'
    bearer_token = os.environ.get("BEARER_TOKEN")
    if not bearer_token:
        return "raise EnvironmentError(BEARER_TOKEN environment variable not set)"
    
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2RecentSearchPython"
    }
    query = {'query': f"{query_params}"}
    response = requests.get(search_url, headers=headers, params=query)
    if response.status_code != 200:
        return "raise Exception(response.status_code, response.text)"
    return "response.json.dumps(json_response, indent=4, sort_keys=True)"

if __name__ == "__main__":
    # This runs the server, defaulting to STDIO transport
    mcp.run()
