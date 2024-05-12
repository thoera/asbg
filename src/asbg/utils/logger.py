import importlib.resources as pkg_resources
import logging
import logging.config
from os import PathLike

import yaml


def get_logger(
    path: PathLike | str | None = None,
    name: str = __name__,
) -> logging.Logger:
    """Gets (or creates) a logger with the correct configuration.

    Args:
        path: The path to the config file to use. Defaults to None.
            If None, the default config file is used.
        name: The name of the logger. Defaults to __name__.

    Returns:
        The logger with the specified name and configuration.
    """
    if path is None:
        ressource = pkg_resources.files("asbg.config").joinpath("logging.yaml")
        with pkg_resources.as_file(ressource) as filename:
            with open(filename, "r") as f:
                cfg = yaml.safe_load(f.read())
    else:
        with open(path, "r") as f:
            cfg = yaml.safe_load(f.read())

    logging.config.dictConfig(cfg)

    return logging.getLogger(name)
