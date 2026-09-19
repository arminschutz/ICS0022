# ICS0022

# Secure File Manager

## Project Scope

Secure File Manager is a command-line application for managing
files within a configured directory.

The planned application will support authentication, file
management and optional file encryption.

## Planned Commands

fileman login
fileman logout
fileman ls
fileman cd <directory>
fileman mkdir <directory>
fileman touch <file>
fileman cat <file>
fileman cp <source> <destination>
fileman mv <source> <destination>
fileman rm <file>
fileman encrypt <file>
fileman decrypt <file>

## Technologies

- Python 3
- cryptography
- argon2-cffi
- pytest

## Installation

Clone the repository:

git clone <repository-url>

Enter the project:

cd secure-file-manager

Create a virtual environment:

python -m venv .venv

Activate the environment:

Linux/macOS:
source .venv/bin/activate

Windows:
.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

## Running

python -m file_manager

## Project Structure

src/       Application source code
tests/     Automated tests
docs/      Architecture documentation
DESIGN.md  Checkpoint 1 design document
