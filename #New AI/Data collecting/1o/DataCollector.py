import requests
import time

WIKI_API = "https://en.wikipedia.org/w/api.php"
OUTPUT_FILE = "InternetData.txt"

# Function to get article titles starting with 'A'
def get_articles_starting_with(letter="A", limit=50, continue_token=None):
    params = {
        "action": "query",
        "list": "allpages",
        "apnamespace": 0,
        "apprefix": letter,
        "aplimit": limit,
        "format": "json"
    }
    if continue_token:
        params["apcontinue"] = continue_token

    response = requests.get(WIKI_API, params=params)
    data = response.json()
    titles = [page["title"] for page in data["query"]["allpages"]]
    next_token = data.get("continue", {}).get("apcontinue", None)
    return titles, next_token

# Function to get plain text of an article
def get_article_text(title):
    params = {
        "action": "query",
        "prop": "extracts",
        "explaintext": True,
        "titles": title,
        "format": "json"
    }
    response = requests.get(WIKI_API, params=params)
    data = response.json()
    page = next(iter(data["query"]["pages"].values()))
    return page.get("extract", "")

# Main loop
article_count = 0
max_articles = 1000  # Adjust to go deeper
continue_token = None

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    while article_count < max_articles:
        titles, continue_token = get_articles_starting_with("A", limit=10, continue_token=continue_token)

        for title in titles:
            print(f"Fetching: {title}")
            text = get_article_text(title)
            if text:
                file.write(f"\n=== {title} ===\n{text}\n")
                article_count += 1
                if article_count >= max_articles:
                    break
            time.sleep(1)  # Respectful delay

        if not continue_token:
            break
