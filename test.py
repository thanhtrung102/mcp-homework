import requests

def scrape_web(url: str) -> str:
    """Scrape web page content using Jina reader and return as markdown"""
    jina_url = f"https://r.jina.ai/{url}"
    response = requests.get(jina_url)
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    url = "https://github.com/alexeygrigorev/minsearch"
    content = scrape_web(url)
    print(f"Number of characters: {len(content)}")
    print(f"\nFirst 500 characters:\n{content[:500]}")
