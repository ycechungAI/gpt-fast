import sys
import os
import shutil
from pathlib import Path
import unittest
import json

# Add scripts directory to path to import convert_hf_checkpoint
sys.path.append(os.path.abspath("scripts"))
from convert_hf_checkpoint import convert_hf_checkpoint

class TestConvertSecurity(unittest.TestCase):
    def setUp(self):
        self.checkpoint_dir = Path("checkpoints/test_convert_model")
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        if self.checkpoint_dir.exists():
            shutil.rmtree(self.checkpoint_dir)
        # remove the root checkpoints folder if empty
        checkpoints_root = Path("checkpoints")
        if checkpoints_root.exists() and not any(checkpoints_root.iterdir()):
            shutil.rmtree(checkpoints_root)

    def test_path_traversal_prevention(self):
        """Test that convert_hf_checkpoint prevents path traversal from malicious index file."""

        # Create malicious index
        index_path = self.checkpoint_dir / 'model.safetensors.index.json'
        malicious_path = "../../../../../tmp/malicious.bin"

        with open(index_path, 'w') as f:
            json.dump({"weight_map": {"some_weight": malicious_path}}, f)

        with self.assertRaises(ValueError) as context:
            # use a known model name like "7B" so ModelArgs initialization doesn't fail
            convert_hf_checkpoint(checkpoint_dir=self.checkpoint_dir, model_name="7B")

        self.assertIn("Path traversal detected", str(context.exception))

if __name__ == '__main__':
    unittest.main()
