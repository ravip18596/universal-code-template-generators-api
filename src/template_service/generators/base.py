from abc import ABC, abstractmethod

from template_service.domain import Signature


class CodeGenerator(ABC):
    language: str

    @abstractmethod
    def generate(self, sig: Signature) -> str:
        ...