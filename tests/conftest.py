"""
Shared pytest fixtures for the template-service test suite.
"""

from __future__ import annotations

from typing import Iterator

import pytest
from fastapi.testclient import TestClient

from template_service.main import app


@pytest.fixture(scope="session")
def client() -> Iterator[TestClient]:
    """Reusable FastAPI test client."""
    with TestClient(app) as c:
        yield c