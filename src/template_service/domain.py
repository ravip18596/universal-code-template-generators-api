from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field


Language = Literal["java", "python", "cpp", "javascript"]


class Parameter(BaseModel):
    name: str
    type: str  # DSL token


class Signature(BaseModel):
    function_name: str
    parameters: List[Parameter]
    returns: Parameter


class TemplateRequest(BaseModel):
    question_id: str
    title: str
    description: str
    signature: Signature
    language: Language


class TemplateResponse(BaseModel):
    language: Language
    template: str