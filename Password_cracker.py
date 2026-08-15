import argparse
import hashlib
import time


DEFAULT_WORDLIST = [
    "password",
    "123456",
    "admin",
    "hunter2",
    "qwerty",
    "letmein",
]


def hash_password(password):
    """Return the SHA-256 hash of a password."""
    return hashlib.sha256(password.encode()).hexdigest()


def dictionary_attack(target_hash, wordlist):
    """Attempt to match a target hash using passwords from a wordlist."""
    print("\nStarting dictionary attack simulation...\n")

    for attempt, password in enumerate(wordlist, start=1):
        print(f"Attempt {attempt}: {password}")

        if hash_password(password) == target_hash:
            return password, attempt

    return None, len(wordlist)


def main():
    parser = argparse.ArgumentParser(
        description="Educational password attack demonstration."
    )

    parser.add_argument(
        "--password",
        default="hunter2",
        help="Demo password to test against (default: hunter2)",
    )

    args = parser.parse_args()

    target_hash = hash_password(args.password)

    print("Password Attack Demo")
    print("--------------------")
    print(f"Target SHA-256: {target_hash}")

    start_time = time.time()

    password, attempts = dictionary_attack(
        target_hash,
        DEFAULT_WORDLIST,
    )

    elapsed_time = time.time() - start_time

    if password:
        print(f"\nPassword found: {password}")
        print(f"Attempts: {attempts}")
    else:
        print("\nPassword was not found in the wordlist.")

    print(f"Completed in {elapsed_time:.4f} seconds")


if __name__ == "__main__":
    main()
