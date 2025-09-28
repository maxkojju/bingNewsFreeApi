from typing import List, Optional
import requests
from bs4 import BeautifulSoup


def bing_news_search(query: str) -> Optional[List[str]]:
    """
    Performs a Bing News search for the given query and returns a list of article URLs.

    Args:
        query (str): The search query string.

    Returns:
        Optional[List[str]]: A list of URLs extracted from the search results,
                             or None if an error occurs or no results are found.

    Note:
        This function parses Bing's HTML directly and may break if Bing changes its layout.
        Use of official APIs (e.g., Bing Search API via Azure) is recommended for production.
    """
    if not isinstance(query, str) or not query.strip():
        print("Invalid or empty query provided: %r", query)
        return None

    base_url = "https://www.bing.com/news/search"
    params = {"q": query.strip()}
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0 Safari/537.36"
        )
    }

    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Failed to fetch results from Bing: %s", e)
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    algocore = soup.find(id="algocore")

    if not algocore:
        print("Element with id='algocore' not found in the response HTML.")
        return None

    urls: List[str] = []
    for element in algocore.find_all(attrs={"url": True}):
        raw_url = element.get("url", "").strip()
        if raw_url:
            urls.append(raw_url)

    print("Extracted %d URLs for query: %s", len(urls), query)
    return urls

print(bing_news_search("Kurt Cobain"))
