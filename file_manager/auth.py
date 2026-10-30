"""Minimal local authentication using Argon2id password hashes."""
import json
import os
from pathlib import Path
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, InvalidHashError

_hasher = PasswordHasher()

def app_home() -> Path:
    path = Path(os.environ.get("ICS0022_HOME", Path.home() / ".ics0022")).expanduser()
    path.mkdir(parents=True, exist_ok=True)
    try:
        path.chmod(0o700)
    except OSError:
        pass
    return path

def auth_file() -> Path:
    return app_home() / "users.json"

def user_exists() -> bool:
    return auth_file().is_file()

def register(username: str, password: str) -> None:
    if not username or username.strip() != username or any(c.isspace() for c in username):
        raise ValueError("Username must be non-empty and contain no whitespace.")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    path = auth_file()
    if path.exists():
        raise ValueError("A user is already registered. Use login.")
    data = {"username": username, "password_hash": _hasher.hash(password)}
    _write_json(path, data)

def authenticate(username: str, password: str) -> bool:
    path = auth_file()
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return username == data["username"] and _hasher.verify(data["password_hash"], password)
    except (OSError, ValueError, KeyError, VerificationError, InvalidHashError, TypeError):
        return False

def _write_json(path: Path, data: dict) -> None:
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(data, indent=2), encoding="utf-8")
    try:
        temp.chmod(0o600)
    except OSError:
        pass
    os.replace(temp, path)
