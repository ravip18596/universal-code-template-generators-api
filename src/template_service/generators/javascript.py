from __future__ import annotations

from textwrap import indent

from template_service.domain import Signature
from .base import CodeGenerator


def _dsl_to_js(type_token: str) -> str:
    # Comments only – JS is untyped, but we keep for docs
    mapping = {
        "int": "number",
        "long": "number",
        "float": "number",
        "double": "number",
        "bool": "boolean",
        "string": "string",
        "Graph": "Record<number, number[]>",
    }
    if type_token.endswith("[]"):
        inner = _dsl_to_js(type_token[:-2])
        return f"{inner}[]"
    if type_token.startswith("List<") and type_token.endswith(">"):
        inner = _dsl_to_js(type_token[5:-1])
        return f"{inner}[]"
    if type_token.startswith("Tree<") and type_token.endswith(">"):
        inner = _dsl_to_js(type_token[5:-1])
        return f"TreeNode<{inner}> | null"
    return mapping.get(type_token, "any")


def _build_sig(sig: Signature) -> str:
    args = ", ".join(f"{p.name}: {_dsl_to_js(p.type)}" for p in sig.parameters)
    ret = _dsl_to_js(sig.returns.type)
    return f"{sig.function_name}({args}): {ret}"


class JavaScriptGenerator(CodeGenerator):
    language = "javascript"

    def generate(self, sig: Signature) -> str:
        sig_line = _build_sig(sig)
        js = f"""const {{ stdin }} = require("process");
        const input = JSON.parse(stdin.read());
        {class_if_needed(sig)}
        const solver = new Solution();
        const result = solver.{sig.function_name}({param_mapping(sig)});
        console.log(JSON.stringify(result));
        """
        return js.strip()


def class_if_needed(sig: Signature) -> str:
    return f"""class Solution {{
              {sig_line} {{
                // Write your logic here
                return null;
              }}
            }}""".replace("sig_line", _build_sig(sig))


def param_mapping(sig: Signature) -> str:
    return ", ".join(f"input.{p.name}" for p in sig.parameters)