## 2024-05-24 - [Path Traversal in Checkpoint Conversion]
**Vulnerability:** The `convert_hf_checkpoint.py` script trusted file paths provided in `model.safetensors.index.json` or `pytorch_model.bin.index.json` without validation. A malicious model could include relative paths (e.g., `../secret.txt`) in the index file, causing the script to read arbitrary files from the filesystem when converting checkpoints.
**Learning:** Model configuration files (like index JSONs) are untrusted user input and must be validated before use, especially when they contain file paths.
**Prevention:** Always resolve paths to absolute paths and verify they are contained within the expected directory using `path.relative_to(base_path)` (wrapped in try/except for robustness) before accessing them.
## 2025-02-18 - Path Traversal in Download Script
**Vulnerability:** Path Traversal in `scripts/download.py` allows arbitrary directory creation via `repo_id`.
**Learning:** Utilities that handle file paths based on user input, even in local scripts, must validate that the output path stays within expected boundaries.
**Prevention:** Use `pathlib.Path.resolve()` to canonicalize paths and check that the target path is within the intended root directory.

## 2025-02-18 - Path Traversal in Checkpoint Conversion
**Vulnerability:** Path Traversal in `scripts/convert_hf_checkpoint.py` allows reading/processing arbitrary files via a malicious HuggingFace model index.
**Learning:** Model index files (like `model.safetensors.index.json`) are untrusted user input and any file paths specified within them must be validated before being used to open or read files.
**Prevention:** Use lexical validation (`path.is_absolute() or '..' in path.parts`) to ensure the target file is securely within the checkpoint directory.
## 2025-02-18 - Path Traversal in Convert Checkpoint Script
**Vulnerability:** Path Traversal in `scripts/convert_hf_checkpoint.py` allows arbitrary file read via a crafted index JSON file mapping model weights to system paths.
**Learning:** Utilities that parse untrusted checkpoint index files (e.g. from Hugging Face) must validate that the paths they point to are contained within the intended model directory.
**Prevention:** Use `pathlib.Path(bin_file).is_absolute()` and check for `'..'` in `parts` to strictly enforce that paths stay within the expected boundaries.

## 2025-02-18 - Path Traversal via Malicious JSON Checkpoint Index
**Vulnerability:** Path traversal in `scripts/convert_hf_checkpoint.py` allowed arbitrary file reads. The script parsed a `"weight_map"` from a HuggingFace index JSON (like `model.safetensors.index.json`) and concatenated the string values directly to the checkpoint directory path without validation.
**Learning:** Security boundaries can be crossed not just via direct user input, but also through third-party data files (like HuggingFace models/JSONs). Malicious model weights or configuration files can exploit path traversal during the loading or conversion process.
**Prevention:** Always validate paths derived from external configurations or third-party JSONs. For models using symlinks, `Path.resolve()` can cause false positives, so lexical validation (e.g. `if path.is_absolute() or '..' in path.parts:`) is preferred to prevent path traversal while maintaining symlink compatibility.
## 2025-02-20 - Path Traversal in Model Conversion Script
**Vulnerability:** Path Traversal in `scripts/convert_hf_checkpoint.py` allows loading arbitrary files via paths specified in `model.safetensors.index.json`.
**Learning:** Security policy treats model index files (e.g., `model.safetensors.index.json`) as untrusted input requiring path validation to prevent traversal attacks.
**Prevention:** Use `path.relative_to(base_path)` within a `try...except ValueError` block to validate paths derived from index files.

## 2025-02-20 - Lexical Path Validation for Symlinks
**Vulnerability:** Path validation using `Path.resolve()` fails when dealing with symlinked models in HuggingFace cache.
**Learning:** Using `Path.resolve()` resolves symlinks to their actual target directories, which may legitimately reside outside the expected base directory (e.g., in a shared `blobs` folder). This causes strict `relative_to` checks to incorrectly block valid model conversions.
**Prevention:** Instead of filesystem resolution, perform lexical validation on the path itself by checking for absolute paths (`path.is_absolute()`) and directory traversal sequences (`".." in path.parts`), or evaluate relative to base via `(base_dir / path).relative_to(base_dir)` without calling `.resolve()`.
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
