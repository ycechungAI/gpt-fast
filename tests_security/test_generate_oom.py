import unittest
import torch
from unittest.mock import MagicMock
from generate import generate

class TestGenerateOOM(unittest.TestCase):
    def test_prompt_length_exceeds_block_size(self):
        # Create a mock model with a small block_size
        mock_model = MagicMock()
        mock_model.config.block_size = 10

        # Create a prompt longer than block_size
        prompt = torch.randint(0, 100, (1, 15))

        # Expect ValueError when generating
        with self.assertRaises(ValueError) as context:
            generate(
                model=mock_model,
                prompt=prompt,
                max_new_tokens=5,
                batch_size=1,
                interactive=False,
                draft_model=None
            )

        self.assertIn("Prompt length (15) exceeds model block size (10)", str(context.exception))

if __name__ == '__main__':
    unittest.main()
