"""Authenticated file encryption using AES-256-GCM and Argon2id."""
import os
from pathlib import Path
from argon2.low_level import Type, hash_secret_raw
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

MAGIC = b"ICS0022E1"
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32

class CryptoError(Exception):
    """Raised when encrypted data is invalid or the password is incorrect."""

def _derive_key(password: str, salt: bytes) -> bytes:
    return hash_secret_raw(
        secret=password.encode("utf-8"),
        salt=salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=2,
        hash_len=KEY_SIZE,
        type=Type.ID,
    )

def encrypt_bytes(data: bytes, password: str) -> bytes:
    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    key = _derive_key(password, salt)
    ciphertext = AESGCM(key).encrypt(nonce, data, MAGIC)
    return MAGIC + salt + nonce + ciphertext

def decrypt_bytes(blob: bytes, password: str) -> bytes:
    header_len = len(MAGIC) + SALT_SIZE + NONCE_SIZE
    if len(blob) < header_len + 16 or not blob.startswith(MAGIC):
        raise CryptoError("Not a valid ICS0022 encrypted file.")
    offset = len(MAGIC)
    salt = blob[offset:offset + SALT_SIZE]
    nonce = blob[offset + SALT_SIZE:header_len]
    ciphertext = blob[header_len:]
    try:
        return AESGCM(_derive_key(password, salt)).decrypt(nonce, ciphertext, MAGIC)
    except InvalidTag as exc:
        raise CryptoError("Decryption failed: wrong password or file was modified.") from exc

def encrypt_file(source: Path, destination: Path, password: str) -> None:
    destination.write_bytes(encrypt_bytes(source.read_bytes(), password))

def decrypt_file(source: Path, destination: Path, password: str) -> None:
    destination.write_bytes(decrypt_bytes(source.read_bytes(), password))
