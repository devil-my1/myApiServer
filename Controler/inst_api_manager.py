from pathlib import Path
import instagrapi
from instagrapi import Client
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag
import os

from common.logger import logger


cl = Client()

cl.login(os.getenv("INST_USERNAME"), os.getenv("INST_PASSWORD"))


class User:
    def __init__(self, user_name: str = "") -> None:
        """Constructor for use basic method to access Instagram API

        Args:
            user_name (str): seeking user name
        """
        self.user_name = user_name

    def user_info(self):
        """Get Instagram User Info

        Returns:
            dict: user info dictinary
        """
        try:
            user_data = cl.user_info_by_username(self.user_name)
            logger.info("Searching for user [%s]", self.user_name)
            self.user_id = user_data.pk
            logger.info("User ID [%s]", self.user_id)
            return user_data
        except instagrapi.exceptions.UserNotFound as err:
            return {"Error": err}

    def user_stories(self):
        """Get stroies of searched user

        Returns:
            list[Story]: List of all stories
        """
        try:
            if self.user_id:
                stories = cl.user_stories(self.user_id)
                logger.info("User[%s] : stories list [%s]", self.user_name, stories)
                return stories
            else:
                return {"Info": "First check user info to get user stories!"}
        except Exception as err:
            return {"Error": str(err)}

    @classmethod
    def download_story(
        self, url: str = None, story_id: str = None, file_name: str = "{}_story"
    ):
        """Download user stories by url or id

        Args:
            url (str, optional): Story's urs. Defaults to None.
            story_id (str, optional): Story's id. Defaults to None.
            file_name (str, optional): Save downloaded file name. Defaults to "{}_story.mp4".
        """
        folder = Path("./inst_data/stories/")
        if not folder.exists():
            folder.mkdir(parents=True)

        file_name = file_name.format(
            len([file for file in folder.glob("*") if Path.is_file(file)]) + 1
        )
        res = None
        logger.info(
            "Story's filename: [%s] id: [%s] url: [%s]", file_name, story_id, url
        )

        try:
            if story_id:
                res = cl.story_download(story_id, file_name, folder)
            elif url:
                res = cl.story_download_by_url(url, file_name, folder)

            return {"File downloaded path": str(res)}
        except Exception as err:
            return {"Error": str(err)}
