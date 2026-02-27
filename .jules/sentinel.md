## 2024-05-24 - [Path Traversal in Checkpoint Conversion]
**Vulnerability:** The `convert_hf_checkpoint.py` script trusted file paths provided in `model.safetensors.index.json` or `pytorch_model.bin.index.json` without validation. A malicious model could include relative paths (e.g., `../secret.txt`) in the index file, causing the script to read arbitrary files from the filesystem when converting checkpoints.
**Learning:** Model configuration files (like index JSONs) are untrusted user input and must be validated before use, especially when they contain file paths.
**Prevention:** Always resolve paths to absolute paths and verify they are contained within the expected directory using `path.relative_to(base_path)` (wrapped in try/except for robustness) before accessing them.
