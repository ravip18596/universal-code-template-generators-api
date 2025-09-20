from typing import Dict

from .base import CodeGenerator
from .java import JavaGenerator
from .python import PythonGenerator
from .cpp import CppGenerator
from .javascript import JavaScriptGenerator

registry: Dict[str, CodeGenerator] = {
    g.language: g()
    for g in (PythonGenerator, JavaGenerator, CppGenerator, JavaScriptGenerator)
}