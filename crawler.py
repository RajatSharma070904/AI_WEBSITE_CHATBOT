import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
    except Exception as e:
        return None, f"Invalid or unreachable URL: {e}"

    soup = BeautifulSoup(r.text, "html.parser")

    
    for tag in soup(["header", "footer", "nav", "aside", "script", "style"]):
        tag.decompose()

    paragraphs = soup.find_all("p")
    text = " ".join(p.get_text(strip=True) for p in paragraphs)

    title = soup.title.string if soup.title else "No Title"

    if len(text.strip()) < 200:
        return None, "Not enough meaningful content on the page"

    return {"text": text, "title": title}, None
