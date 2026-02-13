## 2025-02-18 - Path Traversal in Download Script
**Vulnerability:** Path Traversal in `scripts/download.py` allows arbitrary directory creation via `repo_id`.
**Learning:** Utilities that handle file paths based on user input, even in local scripts, must validate that the output path stays within expected boundaries.
**Prevention:** Use `pathlib.Path.resolve()` to canonicalize paths and check that the target path is within the intended root directory.

## 2025-02-18 - Path Traversal in Checkpoint Converter
**Vulnerability:** Path Traversal in `scripts/convert_hf_checkpoint.py` allows arbitrary file access via malicious paths in `model.safetensors.index.json`.
**Learning:** Blindly trusting paths in external configuration files can lead to path traversal if those paths are joined with a base directory without validation.
**Prevention:** Always validate that resolved paths from external input stay within the intended directory using `path.is_relative_to(base_path)`.
