"""Configuration for the security-as-code lab.

Secrets are loaded exclusively from environment variables.
Never hardcode credentials in source code.
"""

import os

# Load from environment; fail closed if missing.
APP_API_TOKEN = os.getenv("APP_API_TOKEN")
if not APP_API_TOKEN:
    # In production this would raise; for the lab we allow empty for demo.
    APP_API_TOKEN = None
