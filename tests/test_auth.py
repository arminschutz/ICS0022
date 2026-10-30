import pytest
from file_manager import auth

def test_register_and_authenticate(monkeypatch, tmp_path):
    monkeypatch.setenv("ICS0022_HOME", str(tmp_path / "home"))
    auth.register("alice", "correct horse battery")
    assert auth.authenticate("alice", "correct horse battery")
    assert not auth.authenticate("alice", "wrong password")
    assert not auth.authenticate("bob", "correct horse battery")

def test_reject_short_password(monkeypatch, tmp_path):
    monkeypatch.setenv("ICS0022_HOME", str(tmp_path / "home"))
    with pytest.raises(ValueError):
        auth.register("alice", "short")
