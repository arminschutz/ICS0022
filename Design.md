
# Checkpoint 1 — Design

## Architecture

![System Architecture](documents/architecture.png)

The system consists of a CLI connected to the file manager. The file manager handles file storage and authentication.

* Encrypted files are stored in file storage.
* Password hashes are stored by the authentication component.
* The user enters commands and passwords through the CLI.
* The main trust boundary is between the user and the application.

## Threat Model

| Threat              | Mitigation                                      |
| ------------------- | ----------------------------------------------- |
| Unauthorised access | Require authentication                          |
| Password theft      | Store password hashes using Argon2              |
| File modification   | Use authenticated encryption                    |
| Path traversal      | Validate file paths                             |
| Key exposure        | Do not store keys in source code                |
| Password exposure   | Do not log plaintext passwords                  |
| Nonce reuse         | Generate a new random nonce for each encryption |

## Implementation

**Language:** Python 3

**Libraries:**

* `cryptography` — encryption
* `argon2-cffi` — password hashing
* `pytest` — testing

These libraries provide established security implementations instead of requiring custom cryptographic code.
