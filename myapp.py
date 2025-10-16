#!/usr/bin/env python3
"""
Simple script to run a Django development server
using argparse for host, port, and debug options.
"""

import argparse
import subprocess
import sys
import os


def main():
    # Define command-line arguments
    parser = argparse.ArgumentParser(
        description="Run Django server with custom options"
    )
    parser.add_argument(
        "--port", "-p", default="8000", help="Port number (default: 8000)"
    )
    parser.add_argument(
        "--local", "-l", action="store_true", help="Run on localhost only"
    )
    parser.add_argument(
        "--debug", "-d", action="store_true", help="Enable debug mode (via env var)"
    )
    args = parser.parse_args()

    # Set environment variable for Django debug
    # (You must handle DJANGO_DEBUG in your settings.py if you want this to affect DEBUG)
    if args.debug:
        os.environ["DJANGO_DEBUG"] = "1"
    else:
        os.environ["DJANGO_DEBUG"] = "0"

    # Host: localhost or 0.0.0.0
    host = "127.0.0.1" if args.local else "0.0.0.0"
    port = args.port

    # Build the Django runserver command
    cmd = [sys.executable, "manage.py", "runserver", f"{host}:{port}"]

    print(f"Running Django server at http://{host}:{port} (debug={args.debug}) ...")

    # Run the server (blocking call)
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user.")
    except subprocess.CalledProcessError as e:
        print(f"Error running Django server: {e}")


if __name__ == "__main__":
    main()
