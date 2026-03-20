## 2025-02-18 - Path Traversal in Download Script
**Vulnerability:** Path Traversal in `scripts/download.py` allows arbitrary directory creation via `repo_id`.
**Learning:** Utilities that handle file paths based on user input, even in local scripts, must validate that the output path stays within expected boundaries.
**Prevention:** Use `pathlib.Path.resolve()` to canonicalize paths and check that the target path is within the intended root directory.
## 2025-02-18 - Path Traversal in Convert Checkpoint Script
**Vulnerability:** Path Traversal in `scripts/convert_hf_checkpoint.py` allows arbitrary file read via a crafted index JSON file mapping model weights to system paths.
**Learning:** Utilities that parse untrusted checkpoint index files (e.g. from Hugging Face) must validate that the paths they point to are contained within the intended model directory.
**Prevention:** Use `pathlib.Path(bin_file).is_absolute()` and check for `'..'` in `parts` to strictly enforce that paths stay within the expected boundaries.
