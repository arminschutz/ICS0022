import pytest
from file_manager.storage import PathValidationError, Storage

def test_file_operations(tmp_path):
    root = tmp_path / "managed"
    storage = Storage(root)
    storage.touch("a.txt")
    (root / "a.txt").write_text("hello", encoding="utf-8")
    assert storage.read_file("a.txt") == b"hello"
    storage.copy("a.txt", "b.txt")
    assert (root / "b.txt").read_text() == "hello"
    storage.move("b.txt", "c.txt")
    assert not (root / "b.txt").exists()
    storage.remove("c.txt")
    assert not (root / "c.txt").exists()

def test_path_traversal_rejected(tmp_path):
    storage = Storage(tmp_path / "managed")
    with pytest.raises(PathValidationError):
        storage.resolve("../outside.txt")

def test_directories_cannot_be_removed_as_files(tmp_path):
    storage = Storage(tmp_path / "managed")
    storage.mkdir("folder")
    with pytest.raises(PathValidationError):
        storage.remove("folder")
