import requests

def scrape_web(url: str) -> str:
    """Scrape web page content using Jina reader and return as markdown"""
    jina_url = f"https://r.jina.ai/{url}"
    response = requests.get(jina_url)
    response.raise_for_status()
    return response.text

if __name__ == "__main__":
    url = "https://datatalks.club/"
    print(f"Scraping {url}...")
    content = scrape_web(url)

    # Count occurrences of "data" (case-insensitive)
    count = content.lower().count("data")

    print(f"\nTotal characters: {len(content)}")
    print(f"Occurrences of 'data' (case-insensitive): {count}")

    # Show which answer is closest
    options = [61, 111, 161, 261]
    closest = min(options, key=lambda x: abs(x - count))
    print(f"\nClosest answer: {closest}")
    print(f"\nAnswer options: {options}")
