import json
import os
import urllib.parse
import urllib.request

CDX_ENDPOINT = "https://web.archive.org/cdx/search/cdx"


def build_params(username: str) -> dict[str, str]:
    return {
        "url": f"twitter.com/{username}/status/*",
        "output": "json",
        "fl": "timestamp,original",
        "collapse": "urlkey",
        "sort": "desc",
        # "limit": "10",
    }


def fetch_cdx_rows(username: str) -> list[list[str]]:
    query = urllib.parse.urlencode(build_params(username))
    url = f"{CDX_ENDPOINT}?{query}"
    with urllib.request.urlopen(url) as resp:
        data = json.loads(resp.read().decode("utf-8", errors="replace"))
    return data[1:] if data else []


def write_cdx_rows(username: str, rows: list[list[str]]) -> str:
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{username}.txt")
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write("#pointer=0\n")
        for row in rows:
            timestamp, original = row[0], row[1]
            handle.write(f"{timestamp}\t{original}\n")
    return output_path


__all__ = ["fetch_cdx_rows", "build_params", "write_cdx_rows"]


if __name__ == "__main__":
    username = "NekoMakiQAQ"
    output = write_cdx_rows(username, fetch_cdx_rows(username))
    print(output)
