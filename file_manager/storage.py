"""Path validation and file operations restricted to a managed root."""
import os
import shutil
from pathlib import Path

class PathValidationError(ValueError):
    pass

class Storage:
    def __init__(self, root=None):
        configured = root or os.environ.get("ICS0022_ROOT", "managed_files")
        self.root = Path(configured).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.cwd = self.root

    def resolve(self, value: str, *, must_exist=False) -> Path:
        if not value or "\x00" in value:
            raise PathValidationError("A valid path is required.")
        candidate = Path(value).expanduser()
        if not candidate.is_absolute():
            candidate = self.cwd / candidate
        # resolve() follows symlinks; an outside target is rejected.
        resolved = candidate.resolve(strict=False)
        if not resolved.is_relative_to(self.root):
            raise PathValidationError("Path must stay inside the managed directory.")
        if must_exist and not resolved.exists():
            raise FileNotFoundError(f"Path does not exist: {value}")
        return resolved

    def change_dir(self, value="."):
        path = self.resolve(value, must_exist=True)
        if not path.is_dir():
            raise PathValidationError("The requested path is not a directory.")
        self.cwd = path

    def list_dir(self):
        return sorted(self.cwd.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))

    def mkdir(self, value):
        self.resolve(value).mkdir(parents=False, exist_ok=False)

    def touch(self, value):
        path = self.resolve(value)
        if path.exists():
            raise FileExistsError(f"Path already exists: {value}")
        path.parent.mkdir(parents=False, exist_ok=True)
        path.touch(exist_ok=False)

    def read_file(self, value):
        path = self.resolve(value, must_exist=True)
        if not path.is_file():
            raise PathValidationError("Expected a regular file.")
        return path.read_bytes()

    def copy(self, source, destination):
        src = self.resolve(source, must_exist=True)
        dst = self.resolve(destination)
        if not src.is_file():
            raise PathValidationError("Only regular files can be copied.")
        if dst.exists():
            raise FileExistsError(f"Destination already exists: {destination}")
        shutil.copy2(src, dst)

    def move(self, source, destination):
        src = self.resolve(source, must_exist=True)
        dst = self.resolve(destination)
        if not src.is_file():
            raise PathValidationError("Only regular files can be moved.")
        if dst.exists():
            raise FileExistsError(f"Destination already exists: {destination}")
        shutil.move(str(src), str(dst))

    def remove(self, value):
        path = self.resolve(value, must_exist=True)
        if path.is_dir():
            raise PathValidationError("rm removes files only, not directories.")
        path.unlink()
