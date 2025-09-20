from __future__ import annotations

from textwrap import indent

from template_service.domain import Parameter, Signature
from .base import CodeGenerator


def _dsl_to_java(type_token: str) -> str:
    """DSL → Java type (boxed when necessary)."""
    mapping = {
        "int": "int",
        "long": "long",
        "float": "float",
        "double": "double",
        "bool": "boolean",
        "string": "String",
        "Graph": "Map<Integer, List<Integer>>",
    }
    if type_token.endswith("[]"):
        inner = _dsl_to_java(type_token[:-2])
        # int[] → List<Integer>
        if inner in {"int", "long", "float", "double", "boolean"}:
            boxed = {"int": "Integer", "long": "Long", "float": "Float",
                     "double": "Double", "boolean": "Boolean"}[inner]
            return f"List<{boxed}>"
        return f"List<{inner}>"
    if type_token.startswith("List<") and type_token.endswith(">"):
        inner = _dsl_to_java(type_token[5:-1])
        return f"List<{inner}>"
    if type_token.startswith("Tree<") and type_token.endswith(">"):
        inner = _dsl_to_java(type_token[5:-1])
        return f"TreeNode<{inner}>"
    return mapping.get(type_token, "Object")


def _build_method(sig: Signature) -> str:
    args = ", ".join(f"{_dsl_to_java(p.type)} {p.name}" for p in sig.parameters)
    ret = _dsl_to_java(sig.returns.type)
    return f"public {ret} {sig.function_name}({args})"


class JavaGenerator(CodeGenerator):
    language = "java"

    def generate(self, sig: Signature) -> str:
        imports = self._imports(sig)
        method = _build_method(sig)
        inner = indent(
            f"{method} {{\n"
            "        // Write your logic here\n"
            "        return null;\n"
            "    }}",
            "    ",
        )
        return f"""{imports}
public class Solution {{
{inner}

    public static void main(String[] args) throws Exception {{
        ObjectMapper mapper = new ObjectMapper();
        Map<String, Object> input = mapper.readValue(System.in, Map.class);
        Solution solver = new Solution();
        Object result = solver.{sig.function_name}({param_mapping(sig)});
        System.out.println(mapper.writeValueAsString(result));
    }}
}}"""

    @staticmethod
    def _imports(sig: Signature) -> str:
        needs = {"java.util.*", "java.io.*", "com.fasterxml.jackson.databind.*"}
        if any("Graph" in p.type for p in sig.parameters + [sig.returns]):
            needs.add("java.util.Map")
        lines = "\n".join(f"import {i};" for i in sorted(needs))
        return lines


def param_mapping(sig: Signature) -> str:
    """Build comma-separated extractor from Map<String,Object> for each param."""
    parts = []
    for p in sig.parameters:
        java_type = _dsl_to_java(p.type)
        raw = f"({java_type}) input.get(\"{p.name}\")"
        parts.append(raw)
    return ", ".join(parts)