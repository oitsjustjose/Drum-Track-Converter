"""
@author: Jose Stovall | github.com/oitsjustjose | bsky||@oitsjustjose.com
"""

import logging
import os
import sys


class NoPrintStatements:
    """
    Use in a with block to disable print statemenets within that scope
        Source: https://stackoverflow.com/a/45669280
    """

    def __init__(self, verbose: bool):
        self.verbose = verbose

    def __enter__(self):
        if self.verbose:
            return

        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.verbose:
            return

        sys.stdout.close()
        sys.stdout = self._original_stdout


class CustomFormatter(logging.Formatter):
    """
    A logging colorator
    Source: https://stackoverflow.com/a/56944256
    """

    grey = "\x1b[38;20m"
    info = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(levelname)s] - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: info + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class CliOutput:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(CustomFormatter())
        self.logger.addHandler(ch)

    def info(self, input):
        """Displays an informational message to the preferred output method of choice

        Args:
            input (any): The input to display to the user (will be wrapped into a string)
        """
        self.logger.info(f"{input}")

    def warning(self, input):
        """Displays a warning message to the preferred output method of choice

        Args:
            input (any): The input to display to the user (will be wrapped into a string)
        """
        self.logger.warning(f"{input}")

    def error(self, input):
        """Displays an error message to the preferred output method of choice

        Args:
            input (any): The input to display to the user (will be wrapped into a string)
        """
        self.logger.error(f"{input}")
