#!/usr/bin/env python3
"""My Application"""

_myapp_version = "1.0.0"

import argparse
import subprocess
import sys
import os


def sysinfo():
    """Print system information."""
    print(B := "-" * 17, "System Information", B)
    print("Python version: %s" % sys.version.replace("\n", " "))
    print("Platform: {0}({1})".format(sys.platform, sys.getdefaultencoding()))
    print(f"Executable: {sys.executable}")
    print(B + "-" * (len("System Information") + 2) + B)


def main():
    # Define command-line arguments
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", "-v", action="version", version=_myapp_version)
    parser.add_argument("--sysinf", "-s", help=sysinfo.__doc__, action="store_true")
    parser.add_argument(
        "--webapp", "-w", action="store_true", help="Web application to run "
    )
    parser.add_argument(
        "--port", "-p", default="8000", help="Port number (default: 8000) for web app"
    )
    parser.add_argument(
        "--local", "-l", action="store_true", help="Run on localhost only for web app"
    )
    parser.add_argument(
        "--debug",
        "-d",
        action="store_true",
        help="Enable debug mode (via env var) for web app",
    )
    args = parser.parse_args()

    if args.sysinf:
        sysinfo()
        sys.exit(0)
    elif args.webapp:
        print(f"Starting web application: {args.webapp}")
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
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
