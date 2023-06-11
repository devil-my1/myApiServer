import asyncio
import os
import platform
import nats
import json
import sys

sys.path.append(os.getcwd())

from Controller.anime.anime_api_manager import AnimeManager
from common.logger import logger

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    try:
        # Connect to NATS!
        nc = await nats.connect(
            servers=["nats://185.51.246.205:2222"],
            user="local",
            password="WC00cIJqoBNMje8jHb2pDCrdhPF28IeI",
        )

        js = nc.jetstream()

        anime_news = AnimeManager().get_upcoming_anime_list(
            is_use_cache=True, get_new_only=False
        )

        if len(anime_news.get("animes")) >= 1:
            # Publish a message
            ack = await js.publish(
                "develop.ncm.subject",
                json.dumps(anime_news.get("animes")).encode("utf-8"),
            )
            logger.info(
                "Published message to [{}] with seq: {}".format(ack.stream, ack.seq)
            )

    except Exception as err:
        logger.error(f"Error: {err.with_traceback(err.__traceback__)}")
    finally:
        ...
        # Close NATS connection
        await nc.close()


if __name__ == "__main__":
    [asyncio.run(main())]
