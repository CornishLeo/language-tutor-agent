import os
import pytest
from dotenv import load_dotenv

# Load .env file for integration tests
load_dotenv()


@pytest.fixture(autouse=True)
def check_api_keys(request):
    # Only enforce the API key check if the test is marked as an integration test
    if "integration" in request.keywords:
        if not os.environ.get("GOOGLE_API_KEY"):
            pytest.skip("Skipping integration test: GOOGLE_API_KEY is not set.")
