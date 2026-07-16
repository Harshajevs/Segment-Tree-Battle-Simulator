import os
import tempfile

import pytest

# isolated database per test session, configured before app modules import
_db_path = os.path.join(tempfile.mkdtemp(prefix="battle-test-"), "test.db")
os.environ["DATABASE_URL"] = f"sqlite:///{_db_path}"
os.environ["AI_PROVIDER"] = "local"

from fastapi.testclient import TestClient  # noqa: E402

from app.db.database import init_db  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client():
    init_db()
    with TestClient(app) as test_client:
        yield test_client
