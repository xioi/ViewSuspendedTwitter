import json
import os
import re
import urllib.parse
import urllib.request

from snapshot import build_simplified_tweet_html, fetch_snapshot_content_iframe

CDX_ENDPOINT = "https://web.archive.org/cdx/search/cdx"

username = "NekoMakiQAQ"
params = {
    "url": f"twitter.com/{username}/status/*",
    "output": "json",
    "fl": "timestamp,original",
    "collapse": "urlkey",
    # "sort": "desc", // 加这个就是从最新日期开始，不加就是最老的
    "limit": "10",
}

query = urllib.parse.urlencode(params)
url = f"{CDX_ENDPOINT}?{query}"

with urllib.request.urlopen(url) as resp:
    data = json.loads(resp.read().decode("utf-8", errors="replace"))

rows = data[1:] if data else []


def sanitize_filename(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("_")


for row in rows:
    timestamp, original = row[0], row[1]
    iframe_html = fetch_snapshot_content_iframe(timestamp, original)
    simplified_html = build_simplified_tweet_html(iframe_html)
    safe_original = sanitize_filename(original)
    output_dir = username
    os.makedirs(output_dir, exist_ok=True)
    output_name = f"snapshot_{timestamp}_{safe_original}.html"
    output_path = os.path.join(output_dir, output_name)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(simplified_html)
    print([timestamp, original, output_path])
