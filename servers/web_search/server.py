from mcp.server.fastmcp import FastMCP 
from tavily import TavilyClient
import os 
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("web-search")
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@mcp.tool()
def web_search(query: str, max_results: int = 5) -> list[dict]:
    """
    Search in the web and return summarized results.
    Args:
        query: What search for.
        max_results: Maximum number of searchin results to return.
    """
    response = client.search( query=query, max_results=max_results )
    return [
        {"title": r["title"], "url": r["url"], "content": r["content"]}
        for r in response["results"]
    ]

if __name__ == "__main__":
    mcp.run()