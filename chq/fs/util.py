from pathlib import Path

def create_dir(path: Path, name: str="directory", allow_exists=False):
    if path.is_file():
        raise FileExistsError(f"{name} already exists as a file (at {path})")
    if path.is_dir():
        if not allow_exists:
            raise FileExistsError(f"{name} already exists (at {path})")
        return
    path.mkdir(parents=True, exist_ok=True)

def create_file(path: Path, content: str="", name: str="file", allow_exists=False):
    if path.is_dir():
        raise FileExistsError(f"{name} already exists as a directory (at {path})")
    if path.is_file():
        if not allow_exists:
            raise FileExistsError(f"{name} already exists (at {path})")
        return
    path.write_text(content)
