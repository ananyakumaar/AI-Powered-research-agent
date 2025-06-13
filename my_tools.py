import requests
from langchain_core.tools import tool
from datetime import datetime

# 🔎 Web Search Tool (DuckDuckGo direct API)
@tool
def search(query: str) -> str:
    """Search the web for information using DuckDuckGo."""
    url = f"https://duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Simple extraction of the first result
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("a", class_="result__a")
        if results:
            return results[0].get_text(strip=True) + "\n" + results[0]['href']
        else:
            return "No results found."
    else:
        return f"DuckDuckGo search failed with status {response.status_code}."

# 📚 Wikipedia Lookup Tool (Wikipedia API)
@tool
def wiki(query: str) -> str:
    """Fetch Wikipedia summaries using the Wikipedia API."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No summary found.")
    else:
        return f"Wikipedia lookup failed with status {response.status_code}."

# 📝 Save to Text File Tool
@tool
def save(data: str, filename: str = "research_output.txt") -> str:
    """Save structured research data to a text file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    return f"Data successfully saved to {filename}"

# ✅ Define available tools
tools = [search, wiki, save]
