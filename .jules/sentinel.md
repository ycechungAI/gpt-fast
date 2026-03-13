## 2025-02-18 - Path Traversal in Download Script
**Vulnerability:** Path Traversal in `scripts/download.py` allows arbitrary directory creation via `repo_id`.
**Learning:** Utilities that handle file paths based on user input, even in local scripts, must validate that the output path stays within expected boundaries.
**Prevention:** Use `pathlib.Path.resolve()` to canonicalize paths and check that the target path is within the intended root directory.

## 2025-02-18 - Path Traversal via Malicious JSON Checkpoint Index
**Vulnerability:** Path traversal in `scripts/convert_hf_checkpoint.py` allowed arbitrary file reads. The script parsed a `"weight_map"` from a HuggingFace index JSON (like `model.safetensors.index.json`) and concatenated the string values directly to the checkpoint directory path without validation.
**Learning:** Security boundaries can be crossed not just via direct user input, but also through third-party data files (like HuggingFace models/JSONs). Malicious model weights or configuration files can exploit path traversal during the loading or conversion process.
**Prevention:** Always validate paths derived from external configurations or third-party JSONs. For models using symlinks, `Path.resolve()` can cause false positives, so lexical validation (e.g. `if path.is_absolute() or '..' in path.parts:`) is preferred to prevent path traversal while maintaining symlink compatibility.
