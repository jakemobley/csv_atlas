import pytest
import main


@pytest.fixture
def client(request):
    client = main.app.test_client()
    return client
