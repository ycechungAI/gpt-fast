import json
import os
import unittest
import tempfile
import sys
from pathlib import Path

# Add scripts directory to path to import convert_hf_checkpoint
scripts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if scripts_path not in sys.path:
    sys.path.append(scripts_path)

# Add root directory to path to allow scripts to import model
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)

from convert_hf_checkpoint import convert_hf_checkpoint

class TestConvertCheckpointTraversal(unittest.TestCase):
    def test_path_traversal(self):
        # Setup
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            checkpoint_dir = temp_path / "malicious_checkpoint"
            checkpoint_dir.mkdir()

            # Create a dummy index json
            index_json_path = checkpoint_dir / "model.safetensors.index.json"

            # The path we want to access via traversal
            target_file_rel = "../secret.safetensors"
            target_file_abs = (checkpoint_dir / target_file_rel).resolve()

            # Create the target file (content doesn't matter as we expect failure before read)
            with open(target_file_abs, "w") as f:
                f.write("SECRET_DATA")

            index_data = {
                "weight_map": {
                    "layer1": target_file_rel
                }
            }

            with open(index_json_path, "w") as f:
                json.dump(index_data, f)

            # Now run convert_hf_checkpoint and expect a ValueError
            with self.assertRaises(ValueError) as cm:
                convert_hf_checkpoint(checkpoint_dir=checkpoint_dir, model_name="7B")

            self.assertIn("Path traversal detected", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
