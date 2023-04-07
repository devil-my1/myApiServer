import os
import requests
import json
import jmespath
import lxml
from datetime import date
import sys
from bs4 import BeautifulSoup


sys.path.append(os.getcwd())


from common.logger import logger

BASE_URL = "https://zoro.to"
BASE_PATH = os.path.join(os.getcwd(), "Controller", "anime", "data")

cookies = {
    "cf_clearance": "_zKk_gzfsdKPKF0nyz8YHj6_L.qMug7wW3YFiNstmwQ-1653107896-0-150",
    "zscid": "cc30268a-22bf-4dfe-a476-c993a365146b",
    "userSettings": "{%22auto_play%22:%220%22%2C%22auto_next%22:1%2C%22show_comments_at_home%22:1%2C%22enable_dub%22:0%2C%22anime_name%22:%22jp%22%2C%22play_original_audio%22:0%2C%22public_watch_list%22:0%2C%22notify_ignore_folders%22:[%224%22%2C%225%22]%2C%22auto_skip_intro%22:1}",
    "connect.sid": "s%3A4PWonINApAYWnE3a8MXzoDD8gh15KOXt.V%2BlDAJQVAHX6YHlsXQaEQkJMqRpjjXMdBjG%2BMrXaCI4",
    "_ga": "GA1.1.1658381823.1653016176",
    "__atuvc": "45%7C10%2C44%7C11%2C59%7C12%2C22%7C13%2C24%7C14",
    "__atuvs": "642bfd6166376039003",
    "_ga_EQP67TWZDC": "GS1.1.1680604512.13.1.1680607022.0.0.0",
}

headers = {
    "authority": "zoro.to",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,ru-RU;q=0.6,ru;q=0.5",
    "cache-control": "max-age=0",
    # 'cookie': 'cf_clearance=_zKk_gzfsdKPKF0nyz8YHj6_L.qMug7wW3YFiNstmwQ-1653107896-0-150; zscid=cc30268a-22bf-4dfe-a476-c993a365146b; userSettings={%22auto_play%22:%220%22%2C%22auto_next%22:1%2C%22show_comments_at_home%22:1%2C%22enable_dub%22:0%2C%22anime_name%22:%22jp%22%2C%22play_original_audio%22:0%2C%22public_watch_list%22:0%2C%22notify_ignore_folders%22:[%224%22%2C%225%22]%2C%22auto_skip_intro%22:1}; connect.sid=s%3A4PWonINApAYWnE3a8MXzoDD8gh15KOXt.V%2BlDAJQVAHX6YHlsXQaEQkJMqRpjjXMdBjG%2BMrXaCI4; _ga=GA1.1.1658381823.1653016176; watched_18239=true; __atuvc=45%7C10%2C44%7C11%2C59%7C12%2C22%7C13%2C24%7C14; __atuvs=642bfd6166376039003; _ga_EQP67TWZDC=GS1.1.1680604512.13.1.1680607022.0.0.0',
    "referer": "https://zoro.to/",
    "sec-ch-ua": '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
}


def save_file(file_path, new_animes_json, upcoming_anime_json):
    print(f"Added {len(new_animes_json)} new animes to the list:{new_animes_json}")
    upcoming_anime_json.get("animes").extend(new_animes_json)
    with open(os.path.join(file_path, "upcoming_anime_list.json"), "w+") as file:
        json.dump(upcoming_anime_json, file, indent=4)


def read_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def check_new_animes(json1, json2):
    new_animes = []

    for anime in jmespath.search("animes[*]", json2):
        res = jmespath.search(f"animes[?@ == `{json.dumps(anime)}`]", json1)
        if not res and anime not in new_animes:
            new_animes.append(anime)


def save_cache_of_page():
    file_path = os.path.join(
            BASE_PATH, "html_page_cache", f"upcoming_html_cache_{date.today()}.html"
    )

    try:
        if os.path.exists(file_path):
            return file_path

        response = requests.get(
            BASE_URL + "/top-upcoming", cookies=cookies, headers=headers
        )
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response.text)
            logger.info(f"Cache of page saved into {file_path}")
            return file_path
    except Exception as e:
        logger.error(f"Error while saving cache of page: {e}")


def get_upcoming_anime_list(cache_file_path: str):
    try:
        with open(cache_file_path, "r", encoding="utf-8") as file:
            bs = BeautifulSoup(file.read(), "lxml")

        anime_list = bs.find("div", class_="film_list-wrap").find_all(
            "div", class_="flw-item"
        )
        animes = {"animes": []}

        for anime in anime_list:
            anime_name = anime.find("a", class_="dynamic-name").text
            anime_url = BASE_URL + anime.find("a").get("href")
            anime_img = anime.find("img").get("data-src")
            anime_release_date = anime.find("span", class_="fdi-item fdi-duration").text
            anime_description = (
                anime.find("div", class_="description").text
                if anime.find("div", class_="description")
                else "No description."
            )

            animes.get("animes").append(
                {
                    "name": anime_name.strip(),
                    "url": anime_url,
                    "img": anime_img,
                    "date": anime_release_date,
                    "description": anime_description.strip(),
                }
            )

        logger.info(f"Got {len(animes)} Upcoming animes")
        return animes
    except Exception as e:
        logger.error(
            f"Error while getting upcoming anime list: {e.with_traceback(e.__traceback__)}"
        )


def get_upcoming_animes():
    cached_file_path = save_cache_of_page()
    animes = get_upcoming_anime_list(cached_file_path)
    animes_path = os.path.join(BASE_PATH, "upcoming_anime_list.json")

    with open(animes_path, "w", encoding="utf-8") as file:
        json.dump(animes, file, indent=4)

    logger.info(f"Saved upcoming anime list into {animes_path}")

    return animes
