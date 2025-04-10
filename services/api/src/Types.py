from dataclasses import dataclass
from typing import List, Optional
from pydantic import BaseModel, Field


class TrackModel(BaseModel):
    title: str
    authors: List[str]
    image: str
    url: str
    duration: int 
    
class PlaylistModel(BaseModel):
    title: str 
    image: str | None = None
    tracks: List[TrackModel]

class UserModel(BaseModel):
    user_id : int 
    nickname: str
    favorite_tracks: List[TrackModel]
    playlists: List[int]
