## 2025-02-18 - Path Traversal in Download Script
**Vulnerability:** Path Traversal in `scripts/download.py` allows arbitrary directory creation via `repo_id`.
**Learning:** Utilities that handle file paths based on user input, even in local scripts, must validate that the output path stays within expected boundaries.
**Prevention:** Use `pathlib.Path.resolve()` to canonicalize paths and check that the target path is within the intended root directory.

## 2025-02-18 - Path Traversal in Checkpoint Conversion
**Vulnerability:** Path Traversal in `scripts/convert_hf_checkpoint.py` allows reading arbitrary files via malicious `weight_map` in checkpoint index files.
**Learning:** When processing index files or manifests that reference other files, verify that all referenced paths resolve to locations within the trusted directory.
**Prevention:** Resolve all file paths relative to the checkpoint directory. Use `os.path.abspath` instead of `resolve()` if symlinks (like Hugging Face cache) must be supported, to prevent `..` traversal while allowing valid symlinks.
