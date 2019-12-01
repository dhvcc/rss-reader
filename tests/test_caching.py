from unittest import TestCase, main
from unittest.mock import patch, Mock, mock_open, MagicMock
import rss_reader.caching


class TestCachingModule(TestCase):
    def test_clear_cache(self):
        with patch('rss_reader.caching.remove') as remove_mock:
            self.assertTrue(rss_reader.caching.clear_cache(''))
            remove_mock.side_effect = FileNotFoundError
            self.assertRaises(rss_reader.caching.CacheCleanError, rss_reader.caching.clear_cache, '')
            remove_mock.side_effect = Exception
            self.assertRaises(Exception, rss_reader.caching.clear_cache, '')

    def test_get_cached_news(self):
        with patch('rss_reader.caching.open') as open_mock:
            open_mock.side_effect = FileNotFoundError
            self.assertRaises(rss_reader.caching.CacheCleanError, rss_reader.caching.get_cached_news, '', 1, '')
            open_mock.side_effect = rss_reader.caching.NoNewsError
            self.assertRaises(rss_reader.caching.NoNewsError, rss_reader.caching.get_cached_news, '', 1, '')
            open_mock.side_effect = Exception
            self.assertRaises(Exception, rss_reader.caching.get_cached_news, '', 1, '')

        with patch('rss_reader.caching.open') as open_mock:
            open_mock.read = Mock(return_value='')
            with patch('rss_reader.caching.loads') as loads_mock:
                loads_mock.return_value = {}
                self.assertRaises(rss_reader.caching.NoNewsError, rss_reader.caching.get_cached_news, '', 1, '')


if __name__ == '__main__':
    main()
