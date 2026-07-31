import unittest
import torch
import sys
from pathlib import Path

# Add project root to sys.path to allow importing modules
sys.path.append(str(Path(__file__).parent.parent.resolve()))

from generate import generate

class DummyModel:
    class DummyConfig:
        block_size = 1000
    def __init__(self):
        self.config = self.DummyConfig()

class TestGenerateOOM(unittest.TestCase):
    def test_generate_exceeds_block_size(self):
        model = DummyModel()

        # Create a prompt that exceeds the block size
        prompt = torch.zeros((1, 1010), dtype=torch.int)

        # Verify that calling generate with this prompt raises a ValueError
        with self.assertRaises(ValueError) as context:
            generate(model, prompt, 10, 1, interactive=False, draft_model=None)

        self.assertTrue(
            "exceeds model block size" in str(context.exception),
            f"Expected OOM ValueError, got: {context.exception}"
        )

if __name__ == '__main__':
    unittest.main()
