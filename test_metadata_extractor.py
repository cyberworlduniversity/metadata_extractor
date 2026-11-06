import unittest

from metadata_extractor import get_decimal_coordinates, extract_gps_info, extract_metadata


class MetadataExtractorTests(unittest.TestCase):
    def test_southern_and_western_coordinates(self):
        gps = {
            "GPSLatitude": [13, 30, 0],
            "GPSLatitudeRef": "S",
            "GPSLongitude": [80, 15, 0],
            "GPSLongitudeRef": "W",
        }
        self.assertEqual(get_decimal_coordinates(gps), (-13.5, -80.25))

    def test_zero_coordinates_are_valid(self):
        gps = {
            "GPSLatitude": [0, 0, 0],
            "GPSLatitudeRef": "N",
            "GPSLongitude": [0, 0, 0],
            "GPSLongitudeRef": "E",
        }
        self.assertEqual(get_decimal_coordinates(gps), (0.0, 0.0))

    def test_missing_gps_returns_none(self):
        self.assertIsNone(extract_gps_info({}))

    def test_missing_file_returns_error(self):
        result = extract_metadata("this-file-does-not-exist.jpg")
        self.assertIn("error", result)


if __name__ == "__main__":
    unittest.main()
