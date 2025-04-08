from dataclasses import dataclass
from typing import List
from pydantic import BaseModel

class Track(BaseModel):
    title:str
    authors:List[str] # Changed to List[str]
    image:str
    url:str
    duration:int



class Playlist(BaseModel):
    _id:int
    title:str
    author:str
    image:str
    tracks:list[Track]
