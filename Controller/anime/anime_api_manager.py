import os
import requests
import json
import lxml
from datetime import date
import sys
from bs4 import BeautifulSoup


sys.path.append(os.getcwd())


from common.logger import logger


class AnimeManager:
    _BASE_URL = "https://zoro.to"
    _BASE_PATH: str
    _cookies = {
        "cf_clearance": "_zKk_gzfsdKPKF0nyz8YHj6_L.qMug7wW3YFiNstmwQ-1653107896-0-150",
        "zscid": "cc30268a-22bf-4dfe-a476-c993a365146b",
        "userSettings": "{%22auto_play%22:%220%22%2C%22auto_next%22:1%2C%22show_comments_at_home%22:1%2C%22enable_dub%22:0%2C%22anime_name%22:%22jp%22%2C%22play_original_audio%22:0%2C%22public_watch_list%22:0%2C%22notify_ignore_folders%22:[%224%22%2C%225%22]%2C%22auto_skip_intro%22:1}",
        "connect.sid": "s%3A4PWonINApAYWnE3a8MXzoDD8gh15KOXt.V%2BlDAJQVAHX6YHlsXQaEQkJMqRpjjXMdBjG%2BMrXaCI4",
        "_ga": "GA1.1.1658381823.1653016176",
        "__atuvc": "45%7C10%2C44%7C11%2C59%7C12%2C22%7C13%2C24%7C14",
        "__atuvs": "642bfd6166376039003",
        "_ga_EQP67TWZDC": "GS1.1.1680604512.13.1.1680607022.0.0.0",
    }
    _headers = {
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

    def __init__(
        self,
        save_data_base_path: str = os.path.join(
            os.getcwd(), "Controller", "anime", "data"
        ),
    ) -> None:
        self._BASE_PATH = save_data_base_path

    def _extend_animes_list(self, file_path, new_animes_json: dict) -> dict | None:

        upcoming_anime_json = self._read_json_file(file_path)
        if upcoming_anime_json is None:
            logger.error(f"Error while extending anime list")
            return None
        else:
            upcoming_anime_json.get("animes").extend(new_animes_json)
            self._save_file(file_path, upcoming_anime_json)
            logger.debug(
                f"Extended anime list. New length {len(upcoming_anime_json.get('animes'))}"
            )
            return upcoming_anime_json

    def _save_file(self, file_path: str, animes: dict):
        try:
            with open(file_path, "w") as file:
                json.dump(animes, file, indent=4)

                logger.info(f"Saved upcoming anime list into {file_path}")
        except Exception as e:
            logger.error(f"Error while saving file {file_path} {e}")

    def _read_json_file(self, file_path) -> dict | None:
        try:
            if os.path.isfile(file_path):
                with open(file_path, "r") as file:
                    return json.loads(file.read())
        except Exception as e:
            logger.error(f"Error while reading file {file_path} {e}")
            return None

    def _check_new_animes(self, new_animes_list: dict) -> list | None:
        new_animes = []
        old_anime_list = self._read_json_file(
            os.path.join(self._BASE_PATH, "upcoming_anime_list.json")
        )
        if old_anime_list is None:
            return None
        for anime in new_animes_list.get("animes"):
            if anime not in old_anime_list.get("animes") and anime not in new_animes:
                new_animes.append(anime)
        return new_animes

    def _save_cache_of_page(self, url: str):
        file_path = os.path.join(
            self._BASE_PATH,
            "html_page_cache",
            f"upcoming_html_cache_{date.today()}.html",
        )

        try:
            if os.path.exists(file_path):
                return file_path

            response = requests.get(
                self._BASE_URL + url, cookies=self._cookies, headers=self._headers
            )
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response.text)
                logger.info(f"Cache of page saved into {file_path}")
                return file_path
        except Exception as e:
            logger.error(f"Error while saving cache of page: {e}")

    def get_upcoming_anime_list(
        self,
        is_use_cache: bool = True,
        url: str = "/top-upcoming",
        get_new_only: bool = True,
    ):
        try:
            bs = None

            if is_use_cache:
                cached_file_path = self._save_cache_of_page(url)
                with open(cached_file_path, "r", encoding="utf-8") as file:
                    bs = BeautifulSoup(file.read(), "lxml")
            else:
                response = requests.get(
                    self._BASE_URL + url, cookies=self._cookies, headers=self._headers
                )
                bs = BeautifulSoup(response.text, "lxml")

            anime_list = bs.find("div", class_="film_list-wrap").find_all(
                "div", class_="flw-item"
            )
            animes = {"animes": []}

            for anime in anime_list:
                anime_name = anime.find("a", class_="dynamic-name").text
                anime_url = self._BASE_URL + anime.find("a").get("href")
                anime_img = anime.find("img").get("data-src")
                anime_release_date = anime.find(
                    "span", class_="fdi-item fdi-duration"
                ).text
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

            animes_path = os.path.join(self._BASE_PATH, "upcoming_anime_list.json")

            if get_new_only:
                new_animes = self._check_new_animes(animes)

                if new_animes is not None and len(new_animes) > 0:
                    logger.info(f"Got {len(new_animes)} new Upcoming animes")
                    if self._extend_animes_list(animes_path, new_animes) is not None:
                        animes["animes"] = new_animes
                else:
                    logger.info(f"No new upcoming animes")
                    animes["animes"] = []
            else:
                self._save_file(os.path.join(animes_path, animes))

            return animes

        except Exception as e:
            logger.error(
                f"Error while getting upcoming anime list: {e.with_traceback(e.__traceback__)}"
            )
