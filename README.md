# py_pckg_autoloader

Automatically load all modules in a package

## Usage

Content of `__init__.py` of your package:
```python
from py_pckg_autoloader import load_all_modules()

load_all_modules()
```

After this call, your package will have all the modules loaded in the directory and the `__all__` property will contain the modules as well.