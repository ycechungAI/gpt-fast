import unittest
import torch
from model import Transformer, ModelArgs
from generate import generate

class TestGenerateOOM(unittest.TestCase):
    def test_prompt_exceeds_block_size(self):
        config = ModelArgs(block_size=128, vocab_size=1000, n_layer=2, n_head=2, dim=64)
        model = Transformer(config)

        # Create a prompt that exceeds the model's block_size
        prompt = torch.randint(0, 1000, (1, 150))

        with self.assertRaises(ValueError) as context:
            generate(model, prompt, max_new_tokens=10, batch_size=1, interactive=False, draft_model=None)

        self.assertIn("exceeds model block size", str(context.exception))

if __name__ == "__main__":
    unittest.main()
