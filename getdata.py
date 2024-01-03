import requests
import os
import time


def retrieve() -> bool:
    r = requests.get(
        "https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv"
    )

    if r.ok:
        with open("owid-covid-data.csv", "wb") as f:
            f.write(r.content)

        return True

    return False


def refresh() -> bool:
    if os.path.exists("owid-covid-data.csv"):
        # don't refresh data that is less than a day old
        if time.time_ns() - os.stat("owid-covid-data.csv").st_mtime_ns > 864e13:
            return retrieve()

    return retrieve()
