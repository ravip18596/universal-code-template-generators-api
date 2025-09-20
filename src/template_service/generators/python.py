from template_service.domain import Signature
from .base import CodeGenerator

_INDENT = " " * 4


def _dsl_to_py(type_token: str) -> str:
    mapping = {
        "int": "int",
        "long": "int",
        "float": "float",
        "double": "float",
        "bool": "bool",
        "string": "str",
        "Graph": "dict[int, list[int]]",
    }
    if type_token.endswith("[]"):
        inner = _dsl_to_py(type_token[:-2])
        return f"list[{inner}]"
    if type_token.startswith("List<") and type_token.endswith(">"):
        inner = _dsl_to_py(type_token[5:-1])
        return f"list[{inner}]"
    if type_token.startswith("Tree<") and type_token.endswith(">"):
        inner = _dsl_to_py(type_token[5:-1])
        return f"Optional[TreeNode[{inner}]]"
    return mapping.get(type_token, "Any")


def _sig_to_py(sig: Signature) -> str:
    args = ", ".join(
        f"{p.name}: {_dsl_to_py(p.type)}" for p in sig.parameters
    )
    ret = _dsl_to_py(sig.returns.type)
    return f"def {sig.function_name}(self, {args}) -> {ret}:"


class PythonGenerator(CodeGenerator):
    language = "python"

    def generate(self, sig: Signature) -> str:
        method_sig = _sig_to_py(sig)
        return f'''
            class Solution:
            {_INDENT}{method_sig}
            {_INDENT}{_INDENT}# Write your logic here
            {_INDENT}{_INDENT}pass
            
            
            if __name__ == "__main__":
            {_INDENT}import sys, json
            {_INDENT}data = json.loads(sys.stdin.read())
            {_INDENT}sol = Solution()
            {_INDENT}result = sol.{sig.function_name}(**data)
            {_INDENT}print(json.dumps(result))
        '''.strip()