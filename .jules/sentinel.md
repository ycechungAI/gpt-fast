## 2025-02-18 - Path Traversal in Download Script
**Vulnerability:** Path Traversal in `scripts/download.py` allows arbitrary directory creation via `repo_id`.
**Learning:** Utilities that handle file paths based on user input, even in local scripts, must validate that the output path stays within expected boundaries.
**Prevention:** Use `pathlib.Path.resolve()` to canonicalize paths and check that the target path is within the intended root directory.

## 2025-02-18 - Path Traversal in Checkpoint Conversion
**Vulnerability:** Path Traversal in `scripts/convert_hf_checkpoint.py` allows reading/processing arbitrary files via a malicious HuggingFace model index.
**Learning:** Model index files (like `model.safetensors.index.json`) are untrusted user input and any file paths specified within them must be validated before being used to open or read files.
**Prevention:** Use lexical validation (`path.is_absolute() or '..' in path.parts`) to ensure the target file is securely within the checkpoint directory.
