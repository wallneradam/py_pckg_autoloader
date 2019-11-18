import sys
import pkgutil
from importlib import import_module


# noinspection PyProtectedMember
def load_all_modules():
    """
    Load all modules in the directory of the caller
    """
    # Get the context of the caller module
    caller_globals = sys._getframe(1).f_globals
    caller_name = caller_globals['__name__']

    # Create the __all__ magic if not exists
    if '__all__' not in caller_globals:
        caller_globals['__all__'] = []

    # Go through all modules in the directory of the caller
    for info in pkgutil.walk_packages(caller_globals['__path__']):
        if info.ispkg:  # Skip packages
            continue

        module_path = caller_name + '.' + info.name
        if module_path not in sys.modules:
            import_module('.' + info.name, caller_name)

        # Add the module to the globals of the caller module
        caller_globals[info.name] = sys.modules[module_path]
        # Add it to the __all__ magic variable
        caller_globals['__all__'].append(info.name)
