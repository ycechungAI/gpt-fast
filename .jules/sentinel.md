## 2025-02-18 - Path Traversal in Download Script
**Vulnerability:** Path Traversal in `scripts/download.py` allows arbitrary directory creation via `repo_id`.
**Learning:** Utilities that handle file paths based on user input, even in local scripts, must validate that the output path stays within expected boundaries.
**Prevention:** Use `pathlib.Path.resolve()` to canonicalize paths and check that the target path is within the intended root directory.

## 2025-02-18 - Path Traversal in Checkpoint Conversion
**Vulnerability:** Path Traversal in `scripts/convert_hf_checkpoint.py` allows reading arbitrary files via malicious `index.json`.
**Learning:** Model index files (like `model.safetensors.index.json`) can contain relative paths that traverse outside the checkpoint directory. Blindly trusting these paths leads to unauthorized file access.
**Prevention:** Always validate that paths derived from external configuration files resolve to locations within the expected directory, using `path.resolve().is_relative_to()`.
