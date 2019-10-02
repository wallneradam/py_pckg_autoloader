import sys
import pkgutil
from importlib.util import module_from_spec


# noinspection PyProtectedMember
def load_all_modules():
    """
    Load all modules in the directory of the caller
    """
    # Get the context of the caller module
    caller_globals = list(sys._current_frames().values())[-1].f_back.f_globals

    # Create the __all__ magic if not exists
    if '__all__' not in caller_globals:
        caller_globals['__all__'] = []

    # Go through all modules in the directory of the caller
    for info in pkgutil.walk_packages(caller_globals['__path__']):
        if info.ispkg:  # Skip packages
            continue
        module_path = caller_globals['__name__'] + '.' + info.name
        if module_path not in sys.modules:
            # Get module specification
            spec = info.module_finder.find_spec(info.name)
            # Load module without execution
            _module = module_from_spec(spec)
            # Set the parent package to be able to relative import
            _module.__package__ = caller_globals['__package__']
            # Register it into sys.modules
            sys.modules[module_path] = _module
            # Execute the module
            spec.loader.exec_module(_module)

        # Add the module to the globals of the caller module
        caller_globals[info.name] = sys.modules[module_path]
        # Add it to the __all__ magic variable
        caller_globals['__all__'].append(info.name)
