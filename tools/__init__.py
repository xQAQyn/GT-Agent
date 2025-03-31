# __init__.py
import importlib
import pkgutil

tool_list = []

for _, module_name, _ in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f".{module_name}", __package__)
    if hasattr(module, 'tool_list'):
        tool_list.extend(module.tool_list)

__all__ = ['tool_list']
