
import unittest
import tempfile
import shutil
import os
import json
import torch
from pathlib import Path
from safetensors.torch import save_file as save_safetensors_file

# Import the function to test
import sys
sys.path.append(os.path.abspath("scripts"))
# We need to add repo root to sys.path so convert_hf_checkpoint can import model
sys.path.append(os.path.abspath("."))
from convert_hf_checkpoint import convert_hf_checkpoint

class TestConvertTraversal(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.safe_dir = os.path.join(self.test_dir, "safe_dir")
        self.malicious_dir = os.path.join(self.test_dir, "malicious_dir", "checkpoint")

        os.makedirs(self.safe_dir)
        os.makedirs(self.malicious_dir)

        # Create a dummy safetensors file outside the checkpoint dir
        self.secret_file = os.path.join(self.safe_dir, "secret.safetensors")
        tensors = {"weight": torch.zeros((1, 1))}
        save_safetensors_file(tensors, self.secret_file)

        # Create the malicious index file
        self.index_file = os.path.join(self.malicious_dir, "model.safetensors.index.json")
        # Path traversal payload
        payload = os.path.join("..", "..", "safe_dir", "secret.safetensors")

        index_data = {
            "weight_map": {
                "model.embed_tokens.weight": payload
            }
        }

        with open(self.index_file, "w") as f:
            json.dump(index_data, f)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_traversal(self):
        print(f"Testing traversal with checkpoint_dir: {self.malicious_dir}")

        # We expect a ValueError with "Path traversal detected"
        with self.assertRaises(ValueError) as cm:
            convert_hf_checkpoint(
                checkpoint_dir=Path(self.malicious_dir),
                model_name="7B"
            )

        self.assertIn("Path traversal detected", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
