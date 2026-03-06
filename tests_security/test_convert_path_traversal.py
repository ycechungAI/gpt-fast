import sys
import os
import shutil
import json
from pathlib import Path

# Add scripts directory to path
sys.path.append(os.path.abspath("scripts"))
sys.path.append(os.path.abspath("."))
import scripts.convert_hf_checkpoint as convert_module

def test_convert_path_traversal():
    checkpoint_dir = Path("checkpoints/traversal_test_convert")
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    # Create a malicious index file
    malicious_index = {
        "weight_map": {
            "model.embed_tokens.weight": "../../../../../../../../../../../../../tmp/malicious.bin"
        }
    }

    with open(checkpoint_dir / "model.safetensors.index.json", "w") as f:
        json.dump(malicious_index, f)

    from unittest.mock import patch

    with patch("scripts.convert_hf_checkpoint.load_safetensors_file") as mock_load, patch("torch.load") as mock_torch_load, patch("scripts.convert_hf_checkpoint.ModelArgs") as mock_model_args:
        mock_model_args.from_name.return_value = type('obj', (object,), {'dim': 1024, 'head_dim': 128, 'n_head': 8, 'n_local_heads': 8})()

        try:
            convert_module.convert_hf_checkpoint(checkpoint_dir=checkpoint_dir, model_name="dummy")
            print("VULNERABILITY CONFIRMED: Did not catch path traversal.")
            sys.exit(1)
        except ValueError as e:
            if "Path traversal detected" in str(e):
                print("SAFE: Path traversal detected and blocked successfully.")
            else:
                print(f"Unexpected ValueError caught: {e}")
                sys.exit(1)
        except Exception as e:
            print(f"Unexpected Exception caught: {e}")
            sys.exit(1)

if __name__ == "__main__":
    test_convert_path_traversal()
