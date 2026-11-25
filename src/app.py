"""Minimal application demonstrating secure configuration via environment."""

import os
from config import APP_API_TOKEN


def main() -> None:
    token = APP_API_TOKEN or os.getenv("APP_API_TOKEN")
    if not token:
        print("APP_API_TOKEN is not configured.")
        return

    # Never print the token or include it in logs.
    print("Demo application started.")
    print(f"Token configured: {'yes' if bool(token) else 'no'}")


if __name__ == "__main__":
    main()
