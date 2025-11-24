import requests,os
from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient

load_dotenv()

def brave_search(query, limit=1):
    """
    Perform a web search using Brave Search API and return results.

    Args:
        query (str): The search query (e.g., a reference or paper title).
        limit (int): Number of results to return.

    Returns:
        list of dict: Each dict contains 'title' and 'link' keys.
    """
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": os.getenv("BRAVE_SEARCH_API")
    }
    params = {
        "q": query,
        "count": limit
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data['web']['results']:
            results.append({
                "title": item.get("title"),
                "link": item.get("url")
            })
        return results

    except requests.RequestException as e:
        print(f"Error querying Brave Search API: {e}")
        return []

def jina_reader_fetch(url: str) -> str:
    """
    Fetch raw content from a web page using Jina Reader API.

    Args:
        url (str): The URL of the page to fetch.

    Returns:
        str: Extracted content as text.
    """
    # Construct the Jina Reader endpoint
    endpoint = f"https://r.jina.ai/{url}"

    headers = {
        "Authorization": f"Bearer {os.getenv("JINA_READER_API")}"
    }

    try:
        response = requests.get(endpoint, headers=headers, timeout=30)
        response.raise_for_status()
        # Jina Reader usually returns text in JSON format, sometimes under 'content'
        try:
            data = response.json()
            return data.get("content", str(data))
        except ValueError:
            # If response is plain text
            return response.text
    except requests.RequestException as e:
        return f"Error fetching content"
    
@tool
def tavily_search(query: str) -> str:
    """
    Search the web for information.
    args:
    - query (str) : search query

    return:
    - response (dict) : object that included with answer, list of url results, and search score
    """
    client = TavilyClient(api_key=os.getenv("TAVILY_SEARCH_API"))
    response = client.search(
        query=query,
        include_answer="basic",
        max_results=3
    )
    return response
