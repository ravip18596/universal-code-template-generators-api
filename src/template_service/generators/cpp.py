from __future__ import annotations

from textwrap import indent

from template_service.domain import Signature
from .base import CodeGenerator


def _dsl_to_cpp(type_token: str) -> str:
    mapping = {
        "int": "int",
        "long": "long long",
        "float": "float",
        "double": "double",
        "bool": "bool",
        "string": "std::string",
        "Graph": "std::unordered_map<int, std::vector<int>>",
    }
    if type_token.endswith("[]"):
        inner = _dsl_to_cpp(type_token[:-2])
        return f"std::vector<{inner}>"
    if type_token.startswith("List<") and type_token.endswith(">"):
        inner = _dsl_to_cpp(type_token[5:-1])
        return f"std::vector<{inner}>"
    if type_token.startswith("Tree<") and type_token.endswith(">"):
        inner = _dsl_to_cpp(type_token[5:-1])
        return f"TreeNode<{inner}>*"
    return mapping.get(type_token, "auto")


def _build_sig(sig: Signature) -> str:
    args = ", ".join(f"{_dsl_to_cpp(p.type)} {p.name}" for p in sig.parameters)
    ret = _dsl_to_cpp(sig.returns.type)
    return f"{ret} {sig.function_name}({args})"


class CppGenerator(CodeGenerator):
    language = "cpp"

    def generate(self, sig: Signature) -> str:
        sig_line = _build_sig(sig)
        body = indent(
            f"{sig_line} {{\n"
            "    // Write your logic here\n"
            "    return {};\n"
            "}}",
            "    ",
        )
        return f"""#include <bits/stdc++.h>
                #include <nlohmann/json.hpp>
                using json = nlohmann::json;
                
                {class_if_needed(sig)}
                int main() {{
                    json input;
                    std::cin >> input;
                    Solution solver;
                    auto result = solver.{sig.function_name}({param_mapping(sig)});
                    std::cout << json(result).dump();
                    return 0;
                }}"""


def class_if_needed(sig: Signature) -> str:
    """C++ does not require a class, but we keep symmetry."""
    return f"""class Solution {{
            public:
            {indent(_build_sig(sig) + " {\\n    // Write your logic here\\n    return {};\\n}", "    ")}
            }};
            """


def param_mapping(sig: Signature) -> str:
    parts = []
    for p in sig.parameters:
        cpp_type = _dsl_to_cpp(p.type)
        parts.append(f"input[\"{p.name}\"].get<{cpp_type}>()")
    return ", ".join(parts)