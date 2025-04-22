# tools/__init__.py
import importlib
import pkgutil
from typing import List, Any
import sys

def _aggregate_tools() -> List[Any]:
    """智能聚合所有子模块的TOOLS列表"""
    aggregated = []
    
    for module_info in pkgutil.walk_packages(__path__, prefix=__name__ + '.'):
        try:
            module = importlib.import_module(module_info.name)
            
            if module.__name__ == __name__:
                continue
                
            module_tools = getattr(module, "TOOLS", None)
            
            if module_tools is not None:
                if not isinstance(module_tools, list):
                    raise TypeError(
                        f"模块 {module_info.name} 中TOOLS必须是列表类型，当前类型为 {type(module_tools)}"
                    )
                aggregated.extend(module_tools)
                
        except Exception as e:
            sys.stderr.write(f"[WARNING] 加载模块 {module_info.name} 失败: {str(e)}\n")
            continue
            
    return aggregated

TOOLS: List[Any] = _aggregate_tools()
