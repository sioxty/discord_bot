import asyncio
import logging
import disnake
from yt_dlp import YoutubeDL

from .Types import Track


log = logging.getLogger(__name__)


class TrackEngine:
    def __init__(self):
        self._loop = asyncio.get_event_loop()
        self.count_query: int = 2
        self._ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'extract_flat': False,
        }

    async def get_track(self, data: str) -> Track:
        if data.startswith(('http://', 'https://')):
            return await self._search_url(data)
        return await self._search_responce(data)

    async def _search_url(self, url: str):
        info = await self._extract_info(url)
        entries = info.get('entries', [])
        if not entries:
            return None

        return self._format_entry(entries[0])

    async def _search_responce(self, query: str, ):
        info = await self._extract_info(f"ytsearch{self.count_query}:{query}")
        entries = info.get('entries', [])
        if not entries:
            return None

        # Вибрати найкоротший трек
        entries = [e for e in entries if e.get("duration") is not None]
        shortest = min(entries, key=lambda e: e["duration"]) if entries else None
        if shortest is None:
            return None

        return self._format_entry(shortest)

    async def _extract_info(self, source: str):
        def _extract():
            with YoutubeDL(self._ydl_opts) as ydl:
                return ydl.extract_info(source, download=False)

        return await self._loop.run_in_executor(None, _extract)

    def _format_entry(self, entry: dict) -> Track | None:
        if not all(entry.get(key) for key in ('title', 'thumbnail', 'url', 'webpage_url', 'duration')):
            return None
        authors = entry.get('author')
        if not authors:
            authors = entry.get('uploader')
        if isinstance(authors, str):
            authors = [authors]

        return Track(
            title=entry.get('title'),
            authors=authors,
            image=entry.get('thumbnail'),
            url=entry.get('url'),
            web_url=entry.get('webpage_url'),
            duration=entry.get('duration')
        )
