from unittest import TestCase, main
from unittest.mock import patch, Mock
import rss_reader.news


class TestNewsModule(TestCase):
    def test_get_response(self):
        with patch('rss_reader.news.get') as get_mock:
            get_mock.side_effect = Exception
            self.assertRaises(Exception, rss_reader.news.get_response, '')
        with patch('rss_reader.news.get') as get_mock:
            get_mock.return_value = 'value'
            self.assertEqual(rss_reader.news.get_response(''), 'value')

    def test_get_soup(self):
        with patch('rss_reader.news.get_response') as get_mock:
            response_mock = Mock()
            response_mock.content = '<rss></rss>'
            get_mock.return_value = response_mock
            rss_reader.news.get_soup('')
            response_mock.content = ''
            self.assertRaises(rss_reader.news.RSSNotFoundError, rss_reader.news.get_soup, '')

    def test_get_items(self):
        with patch('rss_reader.news.unescape') as unescape_mock:
            unescape_mock.side_effect = Exception
            self.assertRaises(Exception, rss_reader.news.get_items, 1, '')

    def test_print_json(self):
        with patch('rss_reader.news.dumps') as dumps_mock:
            self.assertTrue(rss_reader.news.print_json({}))
            dumps_mock.side_effect = Exception
            self.assertRaises(Exception, rss_reader.news.print_json, {})

    def test_print_regular(self):
        with patch('builtins.print') as print_mock:
            print_mock.side_effect = Exception
            self.assertRaises(Exception, rss_reader.news.print_regular, {})


if __name__ == '__main__':
    main()
