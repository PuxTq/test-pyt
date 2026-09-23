import pytest
import requests
import allure

@pytest.fixture
def dog_api():
    return ApiClient(base_address="https://dog.ceo/api/")