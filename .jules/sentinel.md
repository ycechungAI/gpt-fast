## 2024-05-24 - [Path Traversal in Checkpoint Conversion]
**Vulnerability:** The `convert_hf_checkpoint.py` script trusted file paths provided in `model.safetensors.index.json` or `pytorch_model.bin.index.json` without validation. A malicious model could include relative paths (e.g., `../secret.txt`) in the index file, causing the script to read arbitrary files from the filesystem when converting checkpoints.
**Learning:** Model configuration files (like index JSONs) are untrusted user input and must be validated before use, especially when they contain file paths.
**Prevention:** Always resolve paths to absolute paths and verify they are contained within the expected directory using `path.relative_to(base_path)` (wrapped in try/except for robustness) before accessing them.
## 2025-02-18 - Path Traversal in Download Script
**Vulnerability:** Path Traversal in `scripts/download.py` allows arbitrary directory creation via `repo_id`.
**Learning:** Utilities that handle file paths based on user input, even in local scripts, must validate that the output path stays within expected boundaries.
**Prevention:** Use `pathlib.Path.resolve()` to canonicalize paths and check that the target path is within the intended root directory.

## 2025-02-18 - Path Traversal in Checkpoint Conversion
**Vulnerability:** Path Traversal in `scripts/convert_hf_checkpoint.py` allows reading arbitrary files via malicious `index.json`.
**Learning:** Model index files (like `model.safetensors.index.json`) can contain relative paths that traverse outside the checkpoint directory. Blindly trusting these paths leads to unauthorized file access.
**Prevention:** Always validate that paths derived from external configuration files resolve to locations within the expected directory, using `path.resolve().is_relative_to()`.
## 2025-02-18 - Path Traversal in Checkpoint Converter
**Vulnerability:** Path Traversal in `scripts/convert_hf_checkpoint.py` allows arbitrary file access via malicious paths in `model.safetensors.index.json`.
**Learning:** Blindly trusting paths in external configuration files can lead to path traversal if those paths are joined with a base directory without validation.
**Prevention:** Always validate that resolved paths from external input stay within the intended directory using `path.is_relative_to(base_path)`.
## 2025-02-18 - Path Traversal in Checkpoint Conversion
**Vulnerability:** Path Traversal in `scripts/convert_hf_checkpoint.py` allows reading arbitrary files via malicious `weight_map` in checkpoint index files.
**Learning:** When processing index files or manifests that reference other files, verify that all referenced paths resolve to locations within the trusted directory.
**Prevention:** Resolve all file paths relative to the checkpoint directory. Use `os.path.abspath` instead of `resolve()` if symlinks (like Hugging Face cache) must be supported, to prevent `..` traversal while allowing valid symlinks.
