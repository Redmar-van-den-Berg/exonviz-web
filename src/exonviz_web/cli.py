"""
Module that contains the command line app, so we can still import __main__
without executing side effects
"""

from .app import app


def main() -> None:
    # Pull FLASK_SECRET_KEY from environment, or use fallback random ID
    app.config.from_prefixed_env()
    app.logger.info(f"Secret key: {app.config['SECRET_KEY']}")
    app.run()


if __name__ == "__main__":
    main()
