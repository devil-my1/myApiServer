import datetime
from attr import dataclass


@dataclass()
class InstUser:
    username: str
    full_name: str
    is_private: bool
    profile_pic_url: str
    is_verified: bool
    media_count: int
    follower_count: int
    following_count: int
    biography: str
    accountl_url: str


@dataclass()
class InstMedia:
    id: str
    pl: str
    taken_at: datetime
    location: dict
    like_count: int
    caption_text: str
    video_url: str
    view_count: int
    title: str
