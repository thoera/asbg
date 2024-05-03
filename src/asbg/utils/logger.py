import logging
import logging.config
from os import PathLike

import yaml


def get_logger(
    path: PathLike | str = "logging.yaml",
    name: str = __name__,
) -> logging.Logger:
    """Gets (or creates) a logger with the correct configuration.

    Args:
        path: The path to the file with the config to use. Defaults to "logging.yaml".
        name: The name of the logger. Defaults to __name__.

    Returns:
        The logger with the specified name and configuration.
    """
    with open(path, "r") as f:
        cfg = yaml.safe_load(f.read())

    logging.config.dictConfig(cfg)

    return logging.getLogger(name)
