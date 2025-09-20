import pytest
from syrupy import snapshot

from template_service.domain import Parameter, Signature, TemplateRequest
from template_service.generators import registry

scenarios = [
    {
        "name": "fibonacci",
        "sig": Signature(
            function_name="fib",
            parameters=[Parameter(name="n", type="int")],
            returns=Parameter(name="", type="int"),
        ),
    },
    {
        "name": "merge_k_lists",
        "sig": Signature(
            function_name="mergeKLists",
            parameters=[Parameter(name="lists", type="List<List<int>>")],
            returns=Parameter(name="", type="List<int>"),
        ),
    },
    {
        "name": "detect_cycle",
        "sig": Signature(
            function_name="detectCycle",
            parameters=[Parameter(name="graph", type="Graph")],
            returns=Parameter(name="", type="bool"),
        ),
    },
]


@pytest.mark.parametrize("lang", ["python", "java", "cpp", "javascript"])
@pytest.mark.parametrize("scenario", scenarios, ids=lambda s: s["name"])
def test_generator(lang, scenario, snapshot):
    gen = registry[lang]
    code = gen.generate(scenario["sig"])
    assert code == snapshot