import sys
import os
import unittest
from pathlib import Path
import json

sys.path.append(os.path.abspath("scripts"))
from convert_hf_checkpoint import convert_hf_checkpoint

class TestIndexTraversal(unittest.TestCase):
    def setUp(self):
        self.fake_dir = Path("checkpoints/fake-7B")
        os.makedirs(self.fake_dir, exist_ok=True)
        self.index_file = self.fake_dir / "model.safetensors.index.json"
        with open(self.index_file, "w") as f:
            json.dump({"weight_map": {"layer1": "../../../../../etc/passwd"}}, f)

    def tearDown(self):
        if self.index_file.exists():
            os.remove(self.index_file)
        if self.fake_dir.exists():
            os.rmdir(self.fake_dir)

    def test_index_traversal_prevention(self):
        """Test that convert_hf_checkpoint prevents path traversal from malicious index file."""
        with self.assertRaises(ValueError) as context:
            convert_hf_checkpoint(checkpoint_dir=self.fake_dir, model_name="7B")

        self.assertIn("Path traversal detected", str(context.exception))

if __name__ == "__main__":
    unittest.main()
