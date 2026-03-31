
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
sys.path.append(os.path.abspath("."))
from convert_hf_checkpoint import convert_hf_checkpoint

class TestConvertSymlink(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.cache_dir = os.path.join(self.test_dir, "cache_dir")
        self.checkpoint_dir = os.path.join(self.test_dir, "checkpoint_dir")

        os.makedirs(self.cache_dir)
        os.makedirs(self.checkpoint_dir)

        # Create a real file in cache (simulating HF blob)
        self.blob_file = os.path.join(self.cache_dir, "blob.safetensors")
        tensors = {"model.embed_tokens.weight": torch.zeros((1, 1))}
        save_safetensors_file(tensors, self.blob_file)

        # Create a symlink in checkpoint_dir pointing to cache
        self.symlink_file = os.path.join(self.checkpoint_dir, "model.safetensors")
        os.symlink(self.blob_file, self.symlink_file)

        # Create index file pointing to the symlink
        self.index_file = os.path.join(self.checkpoint_dir, "model.safetensors.index.json")
        index_data = {
            "weight_map": {
                "model.embed_tokens.weight": "model.safetensors"
            }
        }
        with open(self.index_file, "w") as f:
            json.dump(index_data, f)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_symlink_allowed(self):
        print(f"Testing symlink allowed with checkpoint_dir: {self.checkpoint_dir}")

        # This should SUCCEED (no path traversal error) because symlinks are valid in HF cache
        try:
            convert_hf_checkpoint(
                checkpoint_dir=Path(self.checkpoint_dir),
                model_name="7B"
            )
        except ValueError as e:
            if "Path traversal detected" in str(e):
                self.fail(f"Valid symlink was blocked: {e}")
            else:
                # Other ValueErrors might happen but not traversal
                pass
        except Exception as e:
            # logic errors expected due to missing weights
            pass

if __name__ == "__main__":
    unittest.main()
