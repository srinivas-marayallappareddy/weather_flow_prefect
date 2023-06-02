import unittest
from unittest.mock import patch
from temperature import get_weather_info, save_weather_info, get_temperature


class TestGetWeatherInfo(unittest.TestCase):

    def test_get_weather_info_success(self):

        zipcode = "75081"

        weather_info = get_weather_info.fn(zipcode)

        self.assertIsNotNone(weather_info['main'])


class TestSaveWeatherInfo(unittest.TestCase):

    def test_save_weather_info_success(self):

        weather_info = {
            "main": {
                "temp": 280.00
            }
        }

        zipcode = "75081"

        filename = save_weather_info.fn(zipcode, weather_info)

        self.assertIsNotNone(filename)

    @patch("builtins.open")
    def test_save_weather_info_failure(self, mock_open):
        # Mock an exception during the file operation

        weather_info = {
            "main": {
                "temp": 280.00
            }
        }

        zipcode = "75081"

        mock_file = mock_open.return_value
        mock_file.__enter__.side_effect = OSError("File Error")

        with self.assertRaises(OSError):
            save_weather_info.fn(weather_info, zipcode)
