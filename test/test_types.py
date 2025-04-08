import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from services.bot.src.Types import Track, QueueTracks
import aiohttp
from PIL import Image
import io
import disnake


class TestTrack(unittest.IsolatedAsyncioTestCase):
    @patch('aiohttp.ClientSession.get')
    async def test_get_preview_success(self, mock_get):
        # Arrange
        mock_response = AsyncMock()
        mock_response.status = 200
        # Create a dummy image for testing
        dummy_image = Image.new('RGB', (200, 100), color='red')
        buffer = io.BytesIO()
        dummy_image.save(buffer, format='JPEG')
        buffer.seek(0)
        mock_response.read.return_value = buffer.getvalue()
        mock_get.return_value.__aenter__.return_value = mock_response

        track = Track(title='Test Title', authors=['Test Author'], image='http://test.com/image.jpg', url='Test URL', web_url='Test Web URL', duration=100)

        # Act
        result = await track.get_preview()

        # Assert
        self.assertIsInstance(result, disnake.File)
        self.assertEqual(result.filename, 'preview.jpg')

    @patch('aiohttp.ClientSession.get')
    async def test_get_preview_failure(self, mock_get):
        # Arrange
        mock_response = AsyncMock()
        mock_response.status = 404
        mock_get.return_value.__aenter__.return_value = mock_response

        track = Track(title='Test Title', authors=['Test Author'], image='http://test.com/image.jpg', url='Test URL', web_url='Test Web URL', duration=100)

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            await track.get_preview()
        self.assertIn("Не вдалося завантажити прев’ю: 404", str(context.exception))

    @patch('aiohttp.ClientSession.get')
    async def test_get_preview_image_processing(self, mock_get):
        # Arrange
        mock_response = AsyncMock()
        mock_response.status = 200
        # Create a dummy image for testing
        dummy_image = Image.new('RGB', (200, 100), color='red')
        buffer = io.BytesIO()
        dummy_image.save(buffer, format='JPEG')
        buffer.seek(0)
        mock_response.read.return_value = buffer.getvalue()
        mock_get.return_value.__aenter__.return_value = mock_response

        track = Track(title='Test Title', authors=['Test Author'], image='http://test.com/image.jpg', url='Test URL', web_url='Test Web URL', duration=100)

        # Act
        result = await track.get_preview()

        # Assert
        self.assertIsInstance(result, disnake.File)
        self.assertEqual(result.filename, 'preview.jpg')
        # Check if the image was cropped correctly
        with Image.open(result.fp) as img:
            self.assertEqual(img.size, (100, 100))

    @patch('aiohttp.ClientSession.get')
    async def test_get_preview_invalid_image(self, mock_get):
        # Arrange
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.read.return_value = b'invalid image data'
        mock_get.return_value.__aenter__.return_value = mock_response

        track = Track(title='Test Title', authors=['Test Author'], image='http://test.com/image.jpg', url='Test URL', web_url='Test Web URL', duration=100)

        # Act & Assert
        with self.assertRaises(Exception) as context:
            await track.get_preview()
        self.assertIn("cannot identify image file", str(context.exception))

class TestQueueTracks(unittest.IsolatedAsyncioTestCase):
    async def test_next(self):
        queue = QueueTracks(_id=1)
        track1 = Track(title='Test Title 1', authors=['Test Author'], image='Test Image 1', url='Test URL 1', web_url='Test Web URL 1', duration=100)
        track2 = Track(title='Test Title 2', authors=['Test Author'], image='Test Image 2', url='Test URL 2', web_url='Test Web URL 2', duration=50)
        await queue.add_in_queue(track1)
        await queue.add_in_queue(track2)

        next_track = await queue.next()
        self.assertEqual(next_track, track1)
        next_track = await queue.next()
        self.assertEqual(next_track, track2)
        next_track = await queue.next()
        self.assertIsNone(next_track)

    async def test_add_in_queue(self):
        queue = QueueTracks(_id=1, max_count=2)
        track1 = Track(title='Test Title 1', authors=['Test Author'], image='Test Image 1', url='Test URL 1', web_url='Test Web URL 1', duration=100)
        track2 = Track(title='Test Title 2', authors=['Test Author'], image='Test Image 2', url='Test URL 2', web_url='Test Web URL 2', duration=50)
        track3 = Track(title='Test Title 3', authors=['Test Author'], image='Test Image 3', url='Test URL 3', web_url='Test Web URL 3', duration=150)

        self.assertFalse(await queue.add_in_queue(track1))
        self.assertFalse(await queue.add_in_queue(track2))
        self.assertTrue(await queue.add_in_queue(track3))
        self.assertEqual(len(queue.tracks), 2)

    async def test_clean(self):
        queue = QueueTracks(_id=1)
        track1 = Track(title='Test Title 1', authors=['Test Author'], image='Test Image 1', url='Test URL 1', web_url='Test Web URL 1', duration=100)
        await queue.add_in_queue(track1)
        await queue.clean()
        self.assertEqual(len(queue.tracks), 0)

if __name__ == '__main__':
    unittest.main()
