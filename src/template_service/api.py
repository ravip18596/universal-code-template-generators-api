from fastapi import APIRouter, HTTPException, status

from template_service.domain import TemplateRequest, TemplateResponse
from template_service.generators import registry

router = APIRouter(prefix="/api/v1", tags=["templates"])


@router.post(
    "/template",
    response_model=TemplateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_template(req: TemplateRequest) -> TemplateResponse:
    gen = registry.get(req.language)
    if not gen:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {req.language}",
        )
    try:
        code = gen.generate(req.signature)
    except Exception as exc:  # DSL syntax, etc.
        raise HTTPException(
            status_code=400,
            detail=f"Template generation failed: {exc}",
        )
    return TemplateResponse(language=req.language, template=code)