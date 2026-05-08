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

class TestConvertIndexSchema(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.checkpoint_dir = Path(self.temp_dir.name) / "malicious_checkpoint"
        self.checkpoint_dir.mkdir()
        self.index_json_path = self.checkpoint_dir / "model.safetensors.index.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_schema_array(self):
        with open(self.index_json_path, "w") as f:
            json.dump(["not", "a", "dict"], f)

        with self.assertRaises(ValueError) as cm:
            convert_hf_checkpoint(checkpoint_dir=self.checkpoint_dir, model_name="7B")

        self.assertIn("Invalid schema in model index", str(cm.exception))

    def test_schema_missing_weight_map(self):
        with open(self.index_json_path, "w") as f:
            json.dump({"other_key": {}}, f)

        with self.assertRaises(ValueError) as cm:
            convert_hf_checkpoint(checkpoint_dir=self.checkpoint_dir, model_name="7B")

        self.assertIn("Invalid schema in model index", str(cm.exception))

    def test_schema_weight_map_not_dict(self):
        with open(self.index_json_path, "w") as f:
            json.dump({"weight_map": "not_a_dict"}, f)

        with self.assertRaises(ValueError) as cm:
            convert_hf_checkpoint(checkpoint_dir=self.checkpoint_dir, model_name="7B")

        self.assertIn("Invalid schema in model index", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
