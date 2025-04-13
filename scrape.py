
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

channel_url = "https://t.me/s/asianarcvip"
response = requests.get(channel_url)
soup = BeautifulSoup(response.text, "html.parser")

posts = []
for msg in soup.select(".tgme_widget_message"):
    media = msg.select_one(".tgme_widget_message_photo_wrap, video, img")
    caption_elem = msg.select_one(".tgme_widget_message_text")
    time_elem = msg.select_one("time")

    media_url = ""
    if media and media.has_attr("style"):
        style = media["style"]
        if "url(" in style:
            media_url = style.split("url(")[1].split(")")[0].replace("'", "")
    elif media and media.has_attr("src"):
        media_url = media["src"]

    caption = caption_elem.text.strip() if caption_elem else ""

    if time_elem and time_elem.has_attr("datetime"):
        timestamp = time_elem["datetime"]
    else:
        timestamp = datetime.now().isoformat()

    if media_url:
        posts.append({
            "media_url": media_url,
            "caption": caption,
            "timestamp": timestamp
        })

with open("feed.json", "w") as f:
    json.dump(posts, f, indent=2)

print(f"✅ Successfully scraped {len(posts)} posts.")
