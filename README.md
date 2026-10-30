# ICS0022 — Secure File Manager

Checkpoint 2 implementation of the Checkpoint 1 design. This Python command-line application manages files inside a configured root directory, authenticates a local user, and encrypts/decrypts files.

## Requirements

- Python 3.10 or newer
- `cryptography` for AES-GCM authenticated encryption
- `argon2-cffi` for Argon2id password hashing and key derivation
- `pytest` for tests

## Install from a clean checkout

```bash
git clone https://github.com/arminschutz/ICS0022.git
cd ICS0022
python -m venv .venv
```

Activate the environment:

**Linux/macOS**
```bash
source .venv/bin/activate
```

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies and the CLI:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Run

Start the interactive CLI:

```bash
python -m file_manager
```

Or, after installing the package, run:

```bash
fileman
```

On first run, use `register` to create an account, then `login`. Commands are entered inside the interactive prompt. Quote paths containing spaces.

| Command | Example | Description |
|---|---|---|
| `help` | `help` | Display commands |
| `register` | `register` | Create the first account |
| `login` / `logout` | `login` | Start/end an authenticated session |
| `ls [path]` | `ls` | List files and directories |
| `cd <path>` | `cd docs` | Change managed working directory |
| `mkdir <name>` | `mkdir notes` | Create a directory |
| `touch <path>` | `touch notes/a.txt` | Create an empty file |
| `cat <path>` | `cat notes/a.txt` | Print a UTF-8 text file |
| `cp <source> <dest>` | `cp a.txt b.txt` | Copy a file |
| `mv <source> <dest>` | `mv a.txt b.txt` | Move/rename a file |
| `rm <path>` | `rm b.txt` | Remove a file (not a directory) |
| `encrypt <path> [output]` | `encrypt notes/a.txt` | Create `notes/a.txt.enc` by default |
| `decrypt <path> [output]` | `decrypt notes/a.txt.enc` | Restore the original filename by default |
| `exit` | `exit` | Quit |

The managed directory defaults to `managed_files` under the current working directory. Set `ICS0022_ROOT` to use a different root. Application account data defaults to `~/.ics0022`; set `ICS0022_HOME` to change it. Set these environment variables before launching the app.

## Run tests

```bash
python -m pytest -q
```

## Security notes and current limitations

- Password hashes are stored using Argon2 via `argon2-cffi`; plaintext passwords are not written to the account file or logged.
- Files use AES-256-GCM authenticated encryption. Each encryption uses a fresh random salt and nonce; the salt and nonce are stored in the encrypted file header.
- Argon2id derives the file key from the authenticated session password and per-file salt. If the password is forgotten or changed, files encrypted with the old password cannot be decrypted. Back up important files before testing.
- The encrypted file format includes a magic header and authenticated encryption rejects wrong passwords and modified ciphertext.
- The account file and encrypted files are local to this machine. This is a basic single-user prototype, not a multi-user security boundary.
- Path resolution rejects paths that resolve outside the configured root, including symlinks pointing outside it. This does not claim protection against every possible local filesystem race.
- Existing destinations are not overwritten by `encrypt`, `decrypt`, `cp`, or `mv`.
- `cat` expects UTF-8 text; use encryption/decryption for arbitrary binary files.
- The prototype does not yet implement password reset, recovery, or key rotation.

## Project structure

```text
ICS0022/
├── file_manager/
│   ├── __init__.py
│   ├── __main__.py
│   ├── auth.py
│   ├── cli.py
│   ├── crypto.py
│   └── storage.py
├── tests/
│   ├── test_auth.py
│   ├── test_crypto.py
│   └── test_storage.py
├── Documents/
├── Design.md
├── PROGRESS.md
├── README.md
├── pyproject.toml
└── requirements.txt
```
