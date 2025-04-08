from dataclasses import dataclass, field
from PIL import Image
import aiohttp
import io
import disnake
from typing import List


@dataclass
class Track:
    title: str
    authors: List[str]  # Changed to List[str]
    image: str
    url: str
    web_url: str
    duration: int

    async def get_preview(self) -> disnake.File:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.image) as resp:
                if resp.status != 200:
                    raise ValueError(f"Не вдалося завантажити прев’ю: {resp.status}")
                data = await resp.read()

        img = Image.open(io.BytesIO(data))
        if not img.format:
            raise ValueError("Не вдалося визначити формат зображення.")

        width, height = img.size
        side = min(width, height)

        left = (width - side) // 2
        top = (height - side) // 2
        right = left + side
        bottom = top + side

        img = img.crop((left, top, right, bottom))

        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)

        return disnake.File(buffer, filename='preview.jpg')


@dataclass
class QueueTracks:
    _id: int
    max_count: int = field(default=50, compare=False)
    tracks: list = field(default_factory=list, compare=False)

    async def next(self) -> Track | None:
        return self.tracks.pop(0) if self.tracks else None  # type: ignore

    async def add_in_queue(self, track: Track) -> bool:
        if len(self.tracks) >= self.max_count:
            return True
        self.tracks.append(track)
        return False

    async def clean(self):
        self.tracks.clear()
