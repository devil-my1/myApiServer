import instagrapi
from instagrapi import Client
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag
import os

from common import logger


cl = Client()

cl.login(os.getenv("INST_USERNAME"), os.getenv("INST_PASSWORD"))


class User:
    def __init__(self, user_name: str) -> None:
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
            return {"Error": err}
