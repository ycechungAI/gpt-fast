
import sys
import os
import shutil
import json
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts directory to path to import the module
sys.path.append(str(Path(__file__).parent.parent / "scripts"))

# Mock imports that might be problematic or slow
# We need to mock safetensors.torch because the script imports it at top level
sys.modules["safetensors"] = MagicMock()
sys.modules["safetensors.torch"] = MagicMock()

# Now import the target function
try:
    from convert_hf_checkpoint import convert_hf_checkpoint
except ImportError:
    # If direct import fails (e.g. due to relative imports in the script), we might need another approach
    # but let's try this first. The script does sys.path.append so it might work if we are lucky.
    pass

class TestConvertPathTraversal(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("tests_security/tmp_traversal_test")
        self.checkpoint_dir = self.test_dir / "checkpoint"
        self.target_file = self.test_dir / "target.txt"

        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

        self.checkpoint_dir.mkdir(parents=True)
        self.target_file.touch()

        # Create malicious JSON
        self.malicious_json = {
            "weight_map": {
                "layer1": "../target.txt"
            }
        }

        with open(self.checkpoint_dir / "model.safetensors.index.json", "w") as f:
            json.dump(self.malicious_json, f)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    @patch("convert_hf_checkpoint.load_safetensors_file")
    @patch("convert_hf_checkpoint.torch.load")
    def test_path_traversal(self, mock_torch_load, mock_safetensors_load):
        # We expect the function to either:
        # 1. (Vulnerable) Call load with the escaped path
        # 2. (Fixed) Raise ValueError or similar before calling load

        try:
            convert_hf_checkpoint(
                checkpoint_dir=self.checkpoint_dir,
                model_name="7B"
            )
        except Exception as e:
            # If it raises an exception, we check if it's the security check
            if "Path traversal detected" in str(e):
                return # Test passed (secure behavior)
            # If it's another error (e.g. file format), we check if load was called
            pass

        # Check if load was called with the escaped path
        # The path would resolve to .../target.txt

        # Check safetensors load
        for call in mock_safetensors_load.call_args_list:
            args, _ = call
            path = Path(args[0]).resolve()
            if path == self.target_file.resolve():
                self.fail(f"VULNERABILITY: Accessed file outside checkpoint directory: {path}")

        # Check torch load
        for call in mock_torch_load.call_args_list:
            args, _ = call
            path = Path(args[0]).resolve()
            if path == self.target_file.resolve():
                self.fail(f"VULNERABILITY: Accessed file outside checkpoint directory: {path}")

if __name__ == "__main__":
    unittest.main()
