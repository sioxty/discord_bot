import unittest
from unittest.mock import MagicMock, patch
from services.bot.src.TrackEngine import TrackEngine


class TestTrackEngine(unittest.IsolatedAsyncioTestCase):
    @patch('services.bot.src.TrackEngine.YoutubeDL')
    async def test_get_track_url(self, mock_youtubedl):
        # Arrange
        mock_ydl = MagicMock()
        mock_youtubedl.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.return_value = {'entries': [{'title': 'Test Title', 'thumbnail': 'Test Image', 'url': 'Test URL', 'webpage_url': 'Test Web URL', 'duration': 100, 'author': 'Test Author'}]}

        engine = TrackEngine()

        # Act
        result = await engine.get_track('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.title, 'Test Title')
        self.assertEqual(result.image, 'Test Image')
        self.assertEqual(result.url, 'Test URL')
        self.assertEqual(result.web_url, 'Test Web URL')
        self.assertEqual(result.duration, 100)
        self.assertEqual(result.authors, ['Test Author'])  # Changed to authors
        mock_ydl.extract_info.assert_called_once_with('https://www.youtube.com/watch?v=dQw4w9WgXcQ', download=False)

    @patch('services.bot.src.TrackEngine.YoutubeDL')
    async def test_get_track_search(self, mock_youtubedl):
        # Arrange
        mock_ydl = MagicMock()
        mock_youtubedl.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.return_value = {'entries': [{'title': 'Test Title', 'thumbnail': 'Test Image', 'url': 'Test URL', 'webpage_url': 'Test Web URL', 'duration': 100, 'author': 'Test Author'},
                                                          {'title': 'Test Title 2', 'thumbnail': 'Test Image 2', 'url': 'Test URL 2', 'webpage_url': 'Test Web URL 2', 'duration': 50, 'author': 'Test Author 2'}]}

        engine = TrackEngine()

        # Act
        result = await engine.get_track('Test Query')

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.title, 'Test Title 2')
        self.assertEqual(result.image, 'Test Image 2')
        self.assertEqual(result.url, 'Test URL 2')
        self.assertEqual(result.web_url, 'Test Web URL 2')
        self.assertEqual(result.duration, 50)
        self.assertEqual(result.authors, ['Test Author 2'])  # Changed to authors
        mock_ydl.extract_info.assert_called_once_with('ytsearch2:Test Query', download=False)

    @patch('services.bot.src.TrackEngine.YoutubeDL')
    async def test_get_track_no_results(self, mock_youtubedl):
        # Arrange
        mock_ydl = MagicMock()
        mock_youtubedl.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.return_value = {'entries': []}

        engine = TrackEngine()

        # Act
        result = await engine.get_track('Nonexistent Query')

        # Assert
        self.assertIsNone(result)

    @patch('services.bot.src.TrackEngine.YoutubeDL')
    async def test_get_track_no_duration(self, mock_youtubedl):
        # Arrange
        mock_ydl = MagicMock()
        mock_youtubedl.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.return_value = {'entries': [{'title': 'Test Title', 'thumbnail': 'Test Image', 'url': 'Test URL', 'webpage_url': 'Test Web URL', 'author': 'Test Author'},
                                                          {'title': 'Test Title 2', 'thumbnail': 'Test Image 2', 'url': 'Test URL 2', 'webpage_url': 'Test Web URL 2', 'duration': 50, 'author': 'Test Author 2'}]}

        engine = TrackEngine()

        # Act
        result = await engine.get_track('Test Query')

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.title, 'Test Title 2')
        self.assertEqual(result.image, 'Test Image 2')
        self.assertEqual(result.url, 'Test URL 2')
        self.assertEqual(result.web_url, 'Test Web URL 2')
        self.assertEqual(result.duration, 50)
        self.assertEqual(result.authors, ['Test Author 2'])  # Changed to authors
        mock_ydl.extract_info.assert_called_once_with('ytsearch2:Test Query', download=False)

    @patch('services.bot.src.TrackEngine.YoutubeDL')
    async def test_get_track_url_no_entries(self, mock_youtubedl):
        # Arrange
        mock_ydl = MagicMock()
        mock_youtubedl.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.return_value = {}

        engine = TrackEngine()

        # Act
        result = await engine.get_track('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        # Assert
        self.assertIsNone(result)

    @patch('services.bot.src.TrackEngine.YoutubeDL')
    async def test_get_track_missing_fields(self, mock_youtubedl):
        # Arrange
        mock_ydl = MagicMock()
        mock_youtubedl.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.return_value = {'entries': [{'title': 'Test Title', 'thumbnail': 'Test Image', 'url': 'Test URL'}]}

        engine = TrackEngine()

        # Act
        result = await engine.get_track('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        # Assert
        self.assertIsNone(result)

    @patch('services.bot.src.TrackEngine.YoutubeDL')
    async def test_get_track_with_uploader(self, mock_youtubedl):
        # Arrange
        mock_ydl = MagicMock()
        mock_youtubedl.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.return_value = {'entries': [{'title': 'Test Title', 'thumbnail': 'Test Image', 'url': 'Test URL', 'webpage_url': 'Test Web URL', 'duration': 100, 'uploader': 'Test Uploader'}]}

        engine = TrackEngine()

        # Act
        result = await engine.get_track('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.authors, ['Test Uploader'])  # Changed to authors
