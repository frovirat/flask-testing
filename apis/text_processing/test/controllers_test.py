"""Test module for locations.dispatcher"""

import unittest
from unittest import mock

from apis.text_processing.controllers import TextProcessingController


class TestLocationDispatcher(unittest.TestCase):
    """
    Unit tests for the LocationDispatcher class
    """

    @mock.patch('apis.text_processing.controllers.ProcessStats')
    def test_get_stats_nominal(self, mock_stats):
        expected_response = {
            'text_processed_stat': mock_stats.return_value.n_text_processed,
            'characters_found': mock_stats.return_value.n_letters_found,
            'words_found':  mock_stats.return_value.n_words_found
        }

        response = TextProcessingController.get_stats()

        self.assertEqual(response, expected_response)

    @mock.patch('apis.text_processing.controllers.ProcessStats')
    def test_reset_stats_nominal(self, mock_stats):
        expected_response = 'OK'

        response = TextProcessingController.reset_stats()

        self.assertEqual(response, expected_response)
        self.assertEqual(mock_stats.return_value.n_text_processed, 0)
        self.assertEqual(mock_stats.return_value.n_letters_found, 0)
        self.assertEqual(mock_stats.return_value.n_words_found, 0)

    @mock.patch('apis.text_processing.controllers.ProcessStats')
    def test_count_elements_nominal(self, mock_stats):
        expected_response = {
            'words': 3,
            'characters': 16
        }
        text = 'Simple text test'
        mock_stats.return_value.n_text_processed = 0
        mock_stats.return_value.n_letters_found = 0
        mock_stats.return_value.n_words_found = 0

        response = TextProcessingController.count_elements(text)

        self.assertEqual(response, expected_response)
        self.assertEqual(mock_stats.return_value.n_text_processed, 1)
        self.assertEqual(mock_stats.return_value.n_letters_found, 16)
        self.assertEqual(mock_stats.return_value.n_words_found, 3)

    @mock.patch('apis.text_processing.controllers.ProcessStats')
    def test_count_elements_none_text_abnormal(self, mock_stats):
        expected_response = {
            'words': 0,
            'characters': 0
        }
        text = None
        mock_stats.return_value.n_text_processed = 0
        mock_stats.return_value.n_letters_found = 0
        mock_stats.return_value.n_words_found = 0

        response = TextProcessingController.count_elements(text)

        self.assertEqual(response, expected_response)
        self.assertEqual(mock_stats.return_value.n_text_processed, 0)
        self.assertEqual(mock_stats.return_value.n_letters_found, 0)
        self.assertEqual(mock_stats.return_value.n_words_found, 0)

    # @mock.patch('apis.text_processing.controllers.ProcessStats')
    # def test_count_elements_empty_text_abnormal(self, mock_stats):
    #     expected_response = {
    #         'words': 0,
    #         'characters': 0
    #     }
    #     text = ""
    #     mock_stats.return_value.n_text_processed = 0
    #     mock_stats.return_value.n_letters_found = 0
    #     mock_stats.return_value.n_words_found = 0

    #     response = TextProcessingController.count_elements(text)

    #     self.assertEqual(response, expected_response)
    #     self.assertEqual(mock_stats.return_value.n_text_processed, 0)
    #     self.assertEqual(mock_stats.return_value.n_letters_found, 0)
    #     self.assertEqual(mock_stats.return_value.n_words_found, 0)

    @mock.patch('apis.text_processing.controllers.ProcessStats')
    def test_count_words_nominal(self, mock_stats):
        expected_response = {
            'words_found': 3
        }
        text = 'Simple text test'
        mock_stats.return_value.n_text_processed = 0
        mock_stats.return_value.n_letters_found = 0
        mock_stats.return_value.n_words_found = 0

        response = TextProcessingController.count_words(text)

        self.assertEqual(response, expected_response)
        self.assertEqual(mock_stats.return_value.n_text_processed, 1)
        self.assertEqual(mock_stats.return_value.n_letters_found, 0)
        self.assertEqual(mock_stats.return_value.n_words_found, 3)

    @mock.patch('apis.text_processing.controllers.ProcessStats')
    def test_count_words_nominal_filters(self, mock_stats):
        expected_response = {
            'words_found': 1
        }
        text = 'Simple text test'
        filters = ['test']
        mock_stats.return_value.n_text_processed = 0
        mock_stats.return_value.n_letters_found = 0
        mock_stats.return_value.n_words_found = 0

        response = TextProcessingController.count_words(text, filters)

        self.assertEqual(response, expected_response)
        self.assertEqual(mock_stats.return_value.n_text_processed, 1)
        self.assertEqual(mock_stats.return_value.n_letters_found, 0)
        self.assertEqual(mock_stats.return_value.n_words_found, 1)


    @mock.patch('apis.text_processing.controllers.ProcessStats')
    def test_count_words_none_text_abnormal(self, mock_stats):
        expected_response = {
            'words_found': 0
        }
        text = None
        mock_stats.return_value.n_text_processed = 0
        mock_stats.return_value.n_letters_found = 0
        mock_stats.return_value.n_words_found = 0

        response = TextProcessingController.count_words(text)

        self.assertEqual(response, expected_response)
        self.assertEqual(mock_stats.return_value.n_text_processed, 0)
        self.assertEqual(mock_stats.return_value.n_letters_found, 0)
        self.assertEqual(mock_stats.return_value.n_words_found, 0)

    @mock.patch('apis.text_processing.controllers.ProcessStats')
    def test_count_words_empty_text_abnormal(self, mock_stats):
        expected_response = {
            'words_found': 0
        }
        text = ""
        mock_stats.return_value.n_text_processed = 0
        mock_stats.return_value.n_letters_found = 0
        mock_stats.return_value.n_words_found = 0

        response = TextProcessingController.count_words(text)

        self.assertEqual(response, expected_response)
        self.assertEqual(mock_stats.return_value.n_text_processed, 1)
        self.assertEqual(mock_stats.return_value.n_letters_found, 0)
        self.assertEqual(mock_stats.return_value.n_words_found, 0)
