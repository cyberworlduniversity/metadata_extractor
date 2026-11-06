import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import metadata_extractor


class MetadataExtractorSafetyTests(unittest.TestCase):
    def test_rejects_oversized_file_before_decoding(self):
        with tempfile.TemporaryDirectory() as directory:
            image_path = Path(directory) / "large.img"
            with image_path.open("wb") as handle:
                handle.truncate(metadata_extractor.MAX_IMAGE_BYTES + 1)
            result = metadata_extractor.extract_metadata(str(image_path))
            self.assertIn("safety limit", result["error"])

    @patch("metadata_extractor.Image.open")
    def test_rejects_excessive_pixel_dimensions(self, image_open):
        image = MagicMock()
        image.__enter__.return_value = image
        image.__exit__.return_value = False
        image.width = 10000
        image.height = 5000
        image_open.return_value = image
        with tempfile.TemporaryDirectory() as directory:
            image_path = Path(directory) / "fake.jpg"
            image_path.write_bytes(b"small")
            result = metadata_extractor.extract_metadata(str(image_path))
            self.assertIn("pixel safety limit", result["error"])
            image_open.assert_called_once()

    def test_report_replaces_symlink_without_overwriting_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            protected = root / "protected.txt"
            protected.write_text("preserve", encoding="utf-8")
            report = root / "report.json"
            report.symlink_to(protected)
            metadata_extractor.save_report({"gps_info": {}}, str(report))
            self.assertFalse(report.is_symlink())
            self.assertEqual(protected.read_text(encoding="utf-8"), "preserve")
            self.assertEqual(json.loads(report.read_text(encoding="utf-8")), {"gps_info": {}})


if __name__ == "__main__":
    unittest.main()
