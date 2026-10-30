# Checkpoint 2 — Progress Note (Week 9)

## Goal
Extend the Checkpoint 1 design into a runnable Python CLI file manager with authentication, file encryption/decryption, input validation, and reproducible setup instructions.

## Implementation delivered in this checkpoint draft
- Interactive CLI with help, register/login/logout, directory listing/navigation, mkdir, touch, cat, copy, move, remove, encrypt, and decrypt commands.
- Argon2 password hashing for the local account.
- AES-256-GCM authenticated encryption with a fresh random salt and nonce for each encrypted file; Argon2id derives the file encryption key from the session password.
- Path resolution constrained to the configured managed root.
- Initial pytest coverage for authentication, encryption/decryption, tampering, and storage path validation.
- README instructions for installation, running, tests, environment variables, and known limitations.

## Verification
Run `python -m pip install -r requirements.txt` followed by `python -m pytest -q`. Also manually test account creation/login, a file encryption/decryption round trip, wrong-password rejection, and attempts to access paths outside the managed root.

## Known limitations
This is a local, single-user prototype. It has no password recovery or key rotation; encrypted files require the same password used at encryption time. File and account backup is the user's responsibility. Review and test the implementation on the target operating systems before treating it as production-ready.
