"""
Module that contains the command line app, so we can still import __main__
without executing side effects
"""

from .app import app


def main() -> None:
    app.secret_key = "super secret key"
    app.run()


if __name__ == "__main__":
    main()
