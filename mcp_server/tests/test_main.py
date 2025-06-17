import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import shutil
import os

# Adjust the path to import app from the parent directory (mcp_server)
import sys

parent_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(parent_dir))
from main import app, PROMPTS_DIR

# Test client
client = TestClient(app)

# Test prompts directory
TEST_PROMPTS_DIR = parent_dir / "test_prompts_temp"


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up a temporary prompts directory for testing."""
    original_prompts_dir = PROMPTS_DIR
    # The next line is problematic because PROMPTS_DIR is not a dependency that can be overridden this way in FastAPI
    # For a simple script like this, monkeypatching main.PROMPTS_DIR is more direct.
    # app.dependency_overrides[PROMPTS_DIR] = lambda: TEST_PROMPTS_DIR

    if TEST_PROMPTS_DIR.exists():
        shutil.rmtree(TEST_PROMPTS_DIR)
    TEST_PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

    (TEST_PROMPTS_DIR / "test_prompt_exists.txt").write_text("This is a test prompt.")
    (TEST_PROMPTS_DIR / "another_prompt.txt").write_text("Another one here.")

    main_module = sys.modules["main"]
    original_main_prompts_dir = getattr(main_module, "PROMPTS_DIR", None)
    setattr(main_module, "PROMPTS_DIR", TEST_PROMPTS_DIR)

    yield

    shutil.rmtree(TEST_PROMPTS_DIR)
    # app.dependency_overrides = {} # No longer needed
    if original_main_prompts_dir is not None:
        setattr(main_module, "PROMPTS_DIR", original_main_prompts_dir)
    else:  # Should not happen if PROMPTS_DIR was defined in main
        delattr(main_module, "PROMPTS_DIR")


def test_get_prompt_success():
    response = client.get("/api/v1/prompts/test_prompt_exists")  # Removed headers
    assert response.status_code == 200
    assert response.json() == {"prompt_text": "This is a test prompt."}


def test_get_prompt_not_found():
    response = client.get("/api/v1/prompts/non_existent_prompt")  # Removed headers
    assert response.status_code == 404
    assert "Prompt not found" in response.json()["detail"]


def test_get_prompt_invalid_name_chars():
    response = client.get("/api/v1/prompts/invalid!name")  # Removed headers
    assert response.status_code == 400
    assert "Task name contains invalid characters" in response.json()["detail"]


def test_get_prompt_path_traversal_attempt_simple():
    response = client.get("/api/v1/prompts/../another_prompt")  # Removed headers
    assert response.status_code == 400
    assert "Task name contains invalid characters" in response.json()["detail"]


def test_get_prompt_path_traversal_encoded():
    response = client.get("/api/v1/prompts/%2E%2E%2Fanother_prompt")  # Removed headers
    assert response.status_code == 400
    assert "Task name contains invalid characters" in response.json()["detail"]


# Removed test_get_prompt_no_api_key and test_get_prompt_wrong_api_key

# To run these tests, navigate to the mcp_server directory and run:
# python -m pytest
