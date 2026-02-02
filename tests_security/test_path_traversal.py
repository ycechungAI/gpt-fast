import sys
import os
import shutil
from unittest.mock import patch, MagicMock

# Add scripts directory to path
sys.path.append(os.path.abspath("scripts"))
from download import hf_download

def test_path_traversal():
    # Setup
    payload = "../traversal_test_dir"
    target_path = os.path.abspath("traversal_test_dir")

    # Clean up if exists
    if os.path.exists(target_path):
        os.rmdir(target_path)

    # Mock snapshot_download to prevent actual network call and download
    with patch('huggingface_hub.snapshot_download') as mock_download:
        try:
            hf_download(repo_id=payload)
        except Exception as e:
            print(f"Exception: {e}")

    # Check if directory was created outside checkpoints
    if os.path.exists(target_path):
        print("VULNERABILITY CONFIRMED: Directory created outside checkpoints folder")
        os.rmdir(target_path)
    else:
        print("SAFE: Directory not created outside checkpoints folder")

if __name__ == "__main__":
    test_path_traversal()
