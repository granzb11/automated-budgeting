"""Logging_methods holder for the initialization of logging configuration."""

import logging


# noinspection PyArgumentList
def setup_logging(verbosity: int):
    """
    Setup logging for module.
    Initializes logging using logging.basicConfig.
    loglevel is set to logging.WARNING - verbosity count

    :param int verbosity: Number of times --verbose was passed
    :return:
    """
    base_loglevel = logging.WARNING # 30
    verbosity = min(verbosity, 2)
    loglevel = base_loglevel - (verbosity * 10)
    logging.basicConfig(
        level=loglevel,
        datefmt="%x",
        style="{",
        format="{asctime} :: {levelname} :: {name}.{funcName} :: {message}",
    )