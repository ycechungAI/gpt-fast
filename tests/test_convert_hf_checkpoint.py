
import unittest
import json
import os
import shutil
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts directory to path
sys.path.append(os.path.abspath("scripts"))
from convert_hf_checkpoint import convert_hf_checkpoint

class TestConvertHFCheckpoint(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path("test_convert_checkpoints").resolve()
        self.checkpoint_dir = self.base_dir / "checkpoint"
        self.outside_dir = self.base_dir / "outside"

        if self.base_dir.exists():
            shutil.rmtree(self.base_dir)

        os.makedirs(self.checkpoint_dir)
        os.makedirs(self.outside_dir)

    def tearDown(self):
        if self.base_dir.exists():
            shutil.rmtree(self.base_dir)

    def test_path_traversal_prevention(self):
        """Test that convert_hf_checkpoint prevents path traversal in index.json."""

        # Create a dummy file outside
        secret_file = self.outside_dir / "secret.pt"
        secret_file.touch()

        # Create malicious index.json
        # We use a path that traverses out of checkpoint_dir
        index_data = {
            "weight_map": {
                "model.embed_tokens.weight": "../outside/secret.pt"
            }
        }

        with open(self.checkpoint_dir / "model.safetensors.index.json", "w") as f:
            json.dump(index_data, f)

        # Mock ModelArgs and torch/safetensors functions
        with patch('convert_hf_checkpoint.ModelArgs') as MockModelArgs, \
             patch('convert_hf_checkpoint.load_safetensors_file') as mock_load_safe, \
             patch('convert_hf_checkpoint.torch.load') as mock_load_torch, \
             patch('convert_hf_checkpoint.torch.save') as mock_save:

            MockModelArgs.from_name.return_value = MagicMock(
                dim=4096, n_head=32, n_local_heads=32, head_dim=128
            )

            # We expect a ValueError (or similar) due to path traversal check
            # Currently it doesn't raise, so this test is expected to fail (or pass if we assert it fails)
            # But the plan is to verify the fix. So I should write the test asserting the fix.

            with self.assertRaises(ValueError) as context:
                convert_hf_checkpoint(checkpoint_dir=self.checkpoint_dir)

            self.assertIn("Path traversal detected", str(context.exception))

if __name__ == '__main__':
    unittest.main()
