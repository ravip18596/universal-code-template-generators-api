# universal-code-template-generators-api
The stack is Python 3.12 + FastAPI + Pydantic v2

## Project Structure

```text
.
├── README.md
├── pyproject.toml
├── src
│   └── template_service
│       ├── __init__.py
│       ├── main.py
│       ├── domain.py
│       ├── generators
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── java.py
│       │   ├── python.py
│       │   ├── cpp.py
│       │   └── javascript.py
│       └── api.py
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   └── test_generators.py
└── .github
    └── workflows
        └── ci.yml
```

## Design Doc

See [design_doc.md](./design_doc.md)