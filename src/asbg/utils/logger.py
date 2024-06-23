import importlib.resources as pkg_resources
import logging
import logging.config

import yaml


def get_logger(name: str) -> logging.Logger:
    """Gets (or creates) a logger with the correct configuration.

    Args:
        name: The name of the logger.

    Returns:
        The logger with the specified name and configuration.
    """
    ressource = pkg_resources.files("asbg.config").joinpath("logging.yaml")
    with pkg_resources.as_file(ressource) as filename:
        with open(filename, "r") as f:
            cfg = yaml.safe_load(f.read())

    logging.config.dictConfig(cfg)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    return logger
