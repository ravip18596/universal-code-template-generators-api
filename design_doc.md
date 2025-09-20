# Design Doc

## Running Locally

```bash
pip install -e .[dev]
template-service
# or
uvicorn template_service.main:app --reload
```

## Extensibility Roadmap

- **Plugin architecture**: drop a new Generator subclass into generators/, register → zero-touch.
- **DSL v2**: support generics Map<K,V>, Optional<T>.
- **AST-based pretty-printing** instead of string concatenation → safer renames.
- **Template versioning**: tag each generator with schema_version, migrate old problems.
- **Rate-limit & cache** (Redis) identical (language, signature) tuples.
