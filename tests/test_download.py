import unittest
import shutil
import os
import sys
from pathlib import Path
from unittest.mock import patch

# Add scripts directory to path to import download
sys.path.append(os.path.abspath("scripts"))
from download import hf_download

class TestDownloadSecurity(unittest.TestCase):
    def setUp(self):
        self.checkpoints_dir = Path("checkpoints").resolve()
        os.makedirs(self.checkpoints_dir, exist_ok=True)
        self.malicious_repo_id = "../outside_checkpoints"
        self.target_outside = (self.checkpoints_dir / self.malicious_repo_id).resolve()

    def tearDown(self):
        if self.target_outside.exists():
            if self.target_outside.is_dir():
                shutil.rmtree(self.target_outside)
            else:
                os.remove(self.target_outside)

    @patch('huggingface_hub.snapshot_download')
    def test_path_traversal_prevention(self, mock_download):
        """Test that hf_download prevents path traversal."""

        # Ensure the target doesn't exist before test
        if self.target_outside.exists():
             shutil.rmtree(self.target_outside)

        with self.assertRaises(ValueError) as context:
            hf_download(repo_id=self.malicious_repo_id)

        self.assertIn("Path traversal detected", str(context.exception))

        # Verify directory was NOT created
        self.assertFalse(self.target_outside.exists(), "Directory should not be created outside checkpoints")

    @patch('huggingface_hub.snapshot_download')
    def test_valid_path(self, mock_download):
        """Test that hf_download allows valid paths."""
        valid_repo_id = "org/model"

        # We don't want to actually download, mocking handles that.
        # We just check it doesn't raise ValueError
        try:
            hf_download(repo_id=valid_repo_id)
        except ValueError:
            self.fail("hf_download raised ValueError unexpectedly for valid path")

        # Verify it tried to create the directory
        expected_dir = self.checkpoints_dir / valid_repo_id
        self.assertTrue(expected_dir.exists())

        # Cleanup
        if expected_dir.exists():
            shutil.rmtree(expected_dir)

if __name__ == '__main__':
    unittest.main()
