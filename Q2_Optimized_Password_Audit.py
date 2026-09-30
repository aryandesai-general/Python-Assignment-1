"""Q2: Password audit with banned-word and pattern checks."""
import re
import sys


def classify_password(password, banned_words):
    # Length is checked first, matching the assignment's short-password example.
    if not 6 <= len(password) <= 12:
        return "WEAK_LENGTH"

    if any(word in password.casefold() for word in banned_words):
        return "COMPROMISED"

    if re.search(r"(.)\1{3,}", password):
        return "WEAK_PATTERN"

    has_lower = any(ch.islower() for ch in password)
    has_upper = any(ch.isupper() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_special = any(ch in "$#@" for ch in password)

    if has_lower and has_upper and has_digit and has_special:
        return "STRONG"
    return "WEAK_PATTERN"


def main():
    try:
        b = int(sys.stdin.readline().strip())
        if b < 1:
            raise ValueError
        banned_words = [sys.stdin.readline().strip().casefold() for _ in range(b)]
        n = int(sys.stdin.readline().strip())
        if n < 1:
            raise ValueError
    except ValueError:
        print("Invalid input.")
        return

    for index in range(1, n + 1):
        password = sys.stdin.readline().rstrip("\n")
        print(f"{index}: {classify_password(password, banned_words)}")


if __name__ == "__main__":
    main()
