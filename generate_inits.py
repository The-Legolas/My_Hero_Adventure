import os
import ast
import argparse
import logging
from typing import List, Set

# --------------------------------------------------------
# SETTINGS
# --------------------------------------------------------
EXCLUDE_DIRS = {"__pycache__", ".git", ".venv", "venv", "node_modules"}
EXCLUDE_PRIVATE = True  # Exclude names starting with '_'
EXCLUDE_NAMES = set()  # Add names to exclude manually (e.g., {"debug_scaling", "rnd"})
LOG_LEVEL = logging.INFO

# --------------------------------------------------------
# UTILITIES
# --------------------------------------------------------
def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else LOG_LEVEL
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

def extract_definitions(filepath: str) -> List[str]:
    """
    Parses a Python file using AST to extract public class and function names only.
    Ignores variables, private names, and excluded names.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
        tree = ast.parse(code, filename=filepath)
    except (IOError, SyntaxError, UnicodeDecodeError) as e:
        logging.warning(f"Skipping {filepath}: {e}")
        return []

    names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            name = node.name
        elif isinstance(node, ast.FunctionDef):
            name = node.name
        else:
            continue

        if EXCLUDE_PRIVATE and name.startswith('_'):
            continue
        if name in EXCLUDE_NAMES:
            continue
        names.append(name)

    return list(set(names))  # Remove duplicates

def write_init_file(directory: str, module_imports: dict, force: bool, dry_run: bool):
    """
    Writes __init__.py with collected imports and a selective __all__ (classes only).
    Checks for existing file and warns unless force is True.
    """
    init_path = os.path.join(directory, "__init__.py")
    exists = os.path.exists(init_path)

    if exists and not force:
        logging.warning(f"Skipping {init_path} (use --force to overwrite)")
        return

    lines = []
    imports = []
    all_list = []

    # Build import lines and __all__ (classes only for brevity)
    for filename, names in module_imports.items():
        if not names:
            continue
        module_name = filename[:-3]  # strip .py
        # Separate classes and functions for potential future customization
        classes = [n for n in names if n[0].isupper()]  # Heuristic: classes start with capital
        functions = [n for n in names if not n[0].isupper()]
        
        # Import all, but __all__ only classes
        if classes or functions:
            import_items = ", ".join(classes + functions)
            imports.append(f"from .{module_name} import {import_items}")
            all_list.extend(classes)  # Only add classes to __all__

    # Prepare content
    content = "\n".join(imports)
    if all_list:
        content += "\n\n__all__ = [\n"
        content += ",\n".join(f'    "{name}"' for name in sorted(set(all_list)))
        content += "\n]\n"
    else:
        content += "\n# No public classes found\n"

    if dry_run:
        logging.info(f"Dry-run: Would write to {init_path}:\n{content}")
    else:
        try:
            with open(init_path, "w", encoding="utf-8") as f:
                f.write(content)
            logging.info(f"Wrote {init_path}")
        except IOError as e:
            logging.error(f"Failed to write {init_path}: {e}")

# --------------------------------------------------------
# MAIN PROCESSOR
# --------------------------------------------------------
def generate_inits(project_root: str, force: bool, dry_run: bool, exclude: List[str]):
    """
    Walk through the project and generate __init__.py files.
    """
    global EXCLUDE_NAMES
    EXCLUDE_NAMES.update(exclude)  # Add CLI exclusions

    if not os.path.isdir(project_root):
        logging.error(f"Project root '{project_root}' is not a directory")
        return

    for root, dirs, files in os.walk(project_root):
        # Skip unwanted folders
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        py_files = [f for f in files if f.endswith(".py") and f != "__init__.py"]
        if not py_files:
            continue

        module_imports = {}

        # Extract names from each file
        for file in py_files:
            file_path = os.path.join(root, file)
            names = extract_definitions(file_path)
            if names:
                module_imports[file] = names

        if module_imports:
            write_init_file(root, module_imports, force, dry_run)

# --------------------------------------------------------
# MAIN
# --------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate refined __init__.py files for a Python project.")
    parser.add_argument("project_root", nargs="?", default=".", help="Root directory of the project (default: current dir)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing __init__.py files")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--exclude", nargs="*", default=[], help="Names to exclude from imports (e.g., debug_scaling rnd)")
    args = parser.parse_args()

    setup_logging(args.verbose)
    generate_inits(args.project_root, args.force, args.dry_run, args.exclude)
