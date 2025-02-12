from os.path import dirname
from types import ModuleType

from pygeneral.exceptions import PathError


def module(module: ModuleType) -> str:
    """Return the path to the module.

    Args:
        module: The module to get the path for.

    Returns:
        The path to the module.

    """
    if hasattr(module, "__file__") and module.__file__:
        return dirname(module.__file__)

    if hasattr(module, "__path__") and module.__path__:
        return module.__path__[0]

    raise PathError(f"The module {module} could not be found.")
