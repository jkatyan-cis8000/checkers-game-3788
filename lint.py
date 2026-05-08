#!/usr/bin/env python3
"""
lint.py - Enforces layer architecture for the Checkers game.

Rules:
1. Every source file lives in exactly one layer directory under src/
2. Imports may only target layers in the file's "may import from" set
3. No file exceeds 300 lines
4. Uses Python's ast module to analyze imports
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

# Define layer hierarchy and allowed imports
# Each layer may import from layers that come before it in the chain
LAYER_ORDER = ["types", "config", "repo", "service", "runtime", "ui"]
CROSS_CUTTING = ["providers", "utils"]

# Allowed imports per layer
ALLOWED_IMPORTS: Dict[str, Set[str]] = {
    "types": {"types"},
    "config": {"types", "config"},
    "repo": {"types", "config", "repo"},
    "service": {"types", "config", "repo", "providers", "service"},
    "runtime": {"types", "config", "repo", "service", "providers", "runtime"},
    "ui": {"types", "config", "service", "runtime", "providers", "ui"},
    "providers": {"types", "config", "utils", "providers"},
    "utils": {"utils"},
}

# All valid layer directories
ALL_LAYERS = set(LAYER_ORDER + CROSS_CUTTING)

# Source directory
SRC_DIR = Path(__file__).parent / "src"


def get_layer(filepath: Path) -> str | None:
    """Determine which layer a file belongs to based on its path."""
    try:
        rel_path = filepath.relative_to(SRC_DIR)
        parts = rel_path.parts
        if parts and parts[0] in ALL_LAYERS:
            return parts[0]
    except ValueError:
        pass
    return None


def get_imports(filepath: Path) -> List[str]:
    """Parse a Python file and return list of imported module names."""
    imports = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content, filename=str(filepath))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module.split(".")[0])
    except SyntaxError:
        pass
    return imports


def get_imported_layer(imp: str, filepath: Path) -> Tuple[str | None, str]:
    """
    Determine which layer an import refers to.
    Returns (layer_name, import_description).
    """
    # Check if import is a direct layer name
    if imp in ALL_LAYERS:
        return imp, imp
    
    # Check if import is from within a layer (e.g., types.board, service.game)
    rel_path = filepath.relative_to(SRC_DIR)
    file_layer = rel_path.parts[0] if rel_path.parts else ""
    
    # If the import starts with the current file's layer, it's internal
    if imp == file_layer:
        return file_layer, imp
    
    # For cross-layer imports, check if it starts with a known layer
    for layer in ALL_LAYERS:
        if imp == layer:
            return layer, imp
    
    return None, imp


def count_lines(filepath: Path) -> int:
    """Count lines in a file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return len(f.readlines())
    except Exception:
        return 0


def lint_file(filepath: Path) -> List[str]:
    """Lint a single file and return list of violations."""
    violations = []
    
    layer = get_layer(filepath)
    if layer is None:
        violations.append(f"{filepath}: File not in a valid layer directory")
        return violations
    
    # Check line count
    line_count = count_lines(filepath)
    if line_count > 300:
        violations.append(f"{filepath}: Exceeds 300 lines ({line_count} lines)")
    
    # Check imports
    imports = get_imports(filepath)
    allowed = ALLOWED_IMPORTS.get(layer, set())
    
    for imp in imports:
        imported_layer, _ = get_imported_layer(imp, filepath)
        
        # Skip if it's a standard library or external import
        if imported_layer is None:
            continue
        
        # Check if this import is allowed
        if imported_layer not in allowed:
            violations.append(
                f"{filepath}: Cannot import '{imported_layer}' from layer '{layer}'. "
                f"Layer '{layer}' may only import from: {', '.join(sorted(allowed))}"
            )
    
    return violations


def find_python_files() -> List[Path]:
    """Find all Python files under src/."""
    python_files = []
    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".py"):
                python_files.append(Path(root) / file)
    return sorted(python_files)


def main() -> int:
    """Run linter and return exit code."""
    all_violations = []
    
    python_files = find_python_files()
    
    for filepath in python_files:
        violations = lint_file(filepath)
        all_violations.extend(violations)
    
    if all_violations:
        print("Linting failed with the following violations:\n")
        for v in all_violations:
            print(f"  {v}")
        print(f"\n{len(all_violations)} violation(s) found.")
        return 1
    
    print(f"lint.py: All {len(python_files)} source file(s) pass linting.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
