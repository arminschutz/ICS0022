import pytest
from file_manager.crypto import CryptoError, decrypt_bytes, encrypt_bytes

def test_encryption_round_trip():
    original = b"hello\x00 secure file"
    encrypted = encrypt_bytes(original, "correct horse battery")
    assert encrypted != original
    assert decrypt_bytes(encrypted, "correct horse battery") == original

def test_wrong_password_rejected():
    encrypted = encrypt_bytes(b"secret", "correct horse battery")
    with pytest.raises(CryptoError):
        decrypt_bytes(encrypted, "incorrect password")

def test_tampered_data_rejected():
    encrypted = bytearray(encrypt_bytes(b"secret", "correct horse battery"))
    encrypted[-1] ^= 1
    with pytest.raises(CryptoError):
        decrypt_bytes(bytes(encrypted), "correct horse battery")

def test_invalid_format_rejected():
    with pytest.raises(CryptoError):
        decrypt_bytes(b"not encrypted", "password")
