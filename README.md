# ICS0022 — Secure File Manager

## Project Scope

A command-line application for managing files inside a configured directory.

The application will support authentication, file management, and file encryption/decryption.

## Planned Commands

```text
fileman login
fileman logout
fileman ls
fileman cd
fileman mkdir
fileman touch
fileman cat
fileman cp
fileman mv
fileman rm
fileman encrypt
fileman decrypt
```

## Technologies

* Python 3
* `cryptography` — encryption
* `argon2-cffi` — password hashing
* `pytest` — testing

## Installation

```bash
git clone <repository-url>
cd secure-file-manager
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows:

```powershell
.venv\Scripts\activate
```

## Running

```bash
python -m file_manager
```

## Project Structure

```text
secure-file-manager/
├── README.md
├── DESIGN.md
├── Documents
```

