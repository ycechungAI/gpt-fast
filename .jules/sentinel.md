## 2025-02-18 - Path Traversal in Download Script
**Vulnerability:** Path Traversal in `scripts/download.py` allows arbitrary directory creation via `repo_id`.
**Learning:** Utilities that handle file paths based on user input, even in local scripts, must validate that the output path stays within expected boundaries.
**Prevention:** Use `pathlib.Path.resolve()` to canonicalize paths and check that the target path is within the intended root directory.

## 2025-02-20 - Path Traversal in Model Conversion Script
**Vulnerability:** Path Traversal in `scripts/convert_hf_checkpoint.py` allows loading arbitrary files via paths specified in `model.safetensors.index.json`.
**Learning:** Security policy treats model index files (e.g., `model.safetensors.index.json`) as untrusted input requiring path validation to prevent traversal attacks.
**Prevention:** Use `path.relative_to(base_path)` within a `try...except ValueError` block to validate paths derived from index files.

## 2025-02-20 - Lexical Path Validation for Symlinks
**Vulnerability:** Path validation using `Path.resolve()` fails when dealing with symlinked models in HuggingFace cache.
**Learning:** Using `Path.resolve()` resolves symlinks to their actual target directories, which may legitimately reside outside the expected base directory (e.g., in a shared `blobs` folder). This causes strict `relative_to` checks to incorrectly block valid model conversions.
**Prevention:** Instead of filesystem resolution, perform lexical validation on the path itself by checking for absolute paths (`path.is_absolute()`) and directory traversal sequences (`".." in path.parts`), or evaluate relative to base via `(base_dir / path).relative_to(base_dir)` without calling `.resolve()`.
