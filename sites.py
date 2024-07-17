# Fetch top500 sites from https://moz.com/top500 with fallback to cache file
import csv
import json
import urllib.request
import urllib.error

from json_logger import log

TOP_SITES_SOURCE = "https://moz.com/top-500/download?table=top500Domains"
CACHE_FILE = "top500.json"

top500 = {}

try:
    log(target="INFO", message=f"updating top500 from {TOP_SITES_SOURCE}")

    req = urllib.request.Request(
        TOP_SITES_SOURCE,
        data=None,
        headers={"User-Agent": "Mozilla/5.0 (OllieJC/findsecuritycontacts.com)"},
    )
    resp = urllib.request.urlopen(req)
    sites = csv.DictReader([l.decode("utf-8") for l in resp.readlines()])

    for site in sites:
        try:
            top500[int(site["Rank"])] = site["Root Domain"]
        except ValueError as e:
            log(target="ERROR", error=e)

    try:
        log(target="INFO", message=f"saving updated top500 list as {CACHE_FILE}")
        with open(CACHE_FILE, "w") as cachefile:
            json.dump(top500, cachefile, indent=2)
    except (OSError, Exception) as e:
        log(target="ERROR", error=e)

except (
    urllib.error.URLError,
    urllib.error.HTTPError,
    urllib.error.ContentTooShortError,
) as e:
    log(target="ERROR", message="fetching top sites failed", error=e)
    log(target="INFO", message=f"falling back to cache file {CACHE_FILE}")

    try:
        with open(CACHE_FILE, "r") as cachefile:
            top500 = {int(k): str(v) for k, v in dict(json.load(cachefile)).items()}
    except ValueError as e:
        log(target="ERROR", message="non-numerical keys in cache file", error=e)
    except (OSError, Exception) as e:
        log(target="ERROR", message="loading of cache file failed", error=e)


if __name__ == "__main__":
    """Print the resulting top500 dictionary when called directly"""
    print(top500)
