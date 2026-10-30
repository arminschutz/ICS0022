"""Interactive command-line interface for ICS0022."""
import getpass
import shlex
import sys
from pathlib import Path

from . import __version__
from . import auth
from .crypto import CryptoError, encrypt_bytes, decrypt_bytes
from .storage import Storage, PathValidationError

HELP = """Commands:
  register                 Create the first local account
  login                    Authenticate
  logout                   End the current session
  ls [path]                List a directory
  cd <path>                Change the working directory
  mkdir <name>             Create a directory
  touch <path>             Create an empty file
  cat <path>               Print a UTF-8 text file
  cp <source> <dest>       Copy a file
  mv <source> <dest>       Move/rename a file
  rm <path>                Remove a file (not a directory)
  encrypt <path> [output]  Encrypt a file (default: <path>.enc)
  decrypt <path> [output]  Decrypt a file (default: remove .enc or append .dec)
  help                     Show this help
  exit                     Quit
Paths are confined to the managed directory. Quote paths containing spaces.
"""

PROTECTED = {"ls", "cd", "mkdir", "touch", "cat", "cp", "mv", "rm", "encrypt", "decrypt"}

def _arity(args, minimum, maximum=None):
    maximum = minimum if maximum is None else maximum
    if not minimum <= len(args) <= maximum:
        raise ValueError("Incorrect number of arguments. Type 'help' for usage.")

def _destination_for_decryption(source: Path) -> Path:
    if source.name.endswith(".enc"):
        return source.with_name(source.name[:-4])
    return source.with_name(source.name + ".dec")

def run_cli():
    storage = Storage()
    username = None
    session_password = None
    print(f"ICS0022 Secure File Manager v{__version__}. Type 'help' for commands.")
    print(f"Managed directory: {storage.root}")
    while True:
        try:
            line = input(f"fileman{'*' if username else ''}:{storage.cwd.name}> ")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        try:
            parts = shlex.split(line)
            if not parts:
                continue
            command, args = parts[0].lower(), parts[1:]
            if command == "exit":
                _arity(args, 0)
                break
            if command == "help":
                _arity(args, 0)
                print(HELP)
                continue
            if command == "register":
                _arity(args, 0)
                if auth.user_exists():
                    print("An account already exists. Use login.")
                    continue
                user = input("Username: ").strip()
                password = getpass.getpass("New password (minimum 8 characters): ")
                confirm = getpass.getpass("Confirm password: ")
                if password != confirm:
                    print("Passwords do not match.")
                    continue
                auth.register(user, password)
                print("Account created. Use login to start a session.")
                continue
            if command == "login":
                _arity(args, 0)
                if not auth.user_exists():
                    print("No account exists. Run 'register' first.")
                    continue
                user = input("Username: ").strip()
                password = getpass.getpass("Password: ")
                if auth.authenticate(user, password):
                    username, session_password = user, password
                    print("Login successful.")
                else:
                    username, session_password = None, None
                    print("Authentication failed.")
                continue
            if command == "logout":
                _arity(args, 0)
                username, session_password = None, None
                print("Logged out.")
                continue
            if command in PROTECTED and username is None:
                print("Please login first.")
                continue

            if command == "ls":
                _arity(args, 0, 1)
                target = storage.resolve(args[0], must_exist=True) if args else storage.cwd
                if not target.is_dir():
                    raise PathValidationError("Expected a directory.")
                for item in sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
                    print(("[D] " if item.is_dir() else "[F] ") + item.name)
            elif command == "cd":
                _arity(args, 1)
                storage.change_dir(args[0])
                print(storage.cwd.relative_to(storage.root) or ".")
            elif command == "mkdir":
                _arity(args, 1)
                storage.mkdir(args[0])
                print("Directory created.")
            elif command == "touch":
                _arity(args, 1)
                storage.touch(args[0])
                print("File created.")
            elif command == "cat":
                _arity(args, 1)
                print(storage.read_file(args[0]).decode("utf-8"))
            elif command in {"cp", "mv"}:
                _arity(args, 2)
                (storage.copy if command == "cp" else storage.move)(*args)
                print("File " + ("copied." if command == "cp" else "moved."))
            elif command == "rm":
                _arity(args, 1)
                storage.remove(args[0])
                print("File removed.")
            elif command == "encrypt":
                _arity(args, 1, 2)
                source = storage.resolve(args[0], must_exist=True)
                if not source.is_file():
                    raise PathValidationError("Expected a regular file.")
                destination = storage.resolve(args[1]) if len(args) == 2 else storage.resolve(args[0] + ".enc")
                if destination.exists():
                    raise FileExistsError(f"Destination already exists: {destination.name}")
                encrypted = encrypt_bytes(source.read_bytes(), session_password)
                destination.write_bytes(encrypted)
                print(f"Encrypted to {destination.relative_to(storage.root)}")
            elif command == "decrypt":
                _arity(args, 1, 2)
                source = storage.resolve(args[0], must_exist=True)
                if not source.is_file():
                    raise PathValidationError("Expected a regular file.")
                destination = storage.resolve(args[1]) if len(args) == 2 else _destination_for_decryption(source)
                if destination.exists():
                    raise FileExistsError(f"Destination already exists: {destination.name}")
                plaintext = decrypt_bytes(source.read_bytes(), session_password)
                destination.write_bytes(plaintext)
                print(f"Decrypted to {destination.relative_to(storage.root)}")
            else:
                print(f"Unknown command: {command}. Type 'help'.")
        except (ValueError, OSError, PathValidationError, CryptoError) as exc:
            print(f"Error: {exc}")
        except Exception as exc:
            # Keep the CLI alive without printing tracebacks to ordinary users.
            print(f"Unexpected error ({type(exc).__name__}). Check the input and try again.")

def main():
    run_cli()

if __name__ == "__main__":
    main()
