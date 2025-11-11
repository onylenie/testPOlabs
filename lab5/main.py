import pytest
import requests
import json

BASE_URL = "https://jsonplaceholder.typicode.com"


class TestAPI:

    def test_get_user(self):
        """Тест для GET запроса - получение пользователя"""
        response = requests.get(f"{BASE_URL}/users/1")

        # Проверка статус кода
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        # Проверка структуры JSON
        json_data = response.json()
        expected_keys = ['id', 'name', 'username', 'email', 'address', 'phone', 'website', 'company']
        for key in expected_keys:
            assert key in json_data, f"Missing key: {key}"

        # Проверка значений полей
        assert json_data['id'] == 1
        assert json_data['name'] == "Leanne Graham"
        assert json_data['email'] == "Sincere@april.biz"

    def test_create_user(self):
        """Тест для POST запроса - создание пользователя"""
        data = {
            "name": "John Doe",
            "username": "johndoe",
            "email": "john@example.com"
        }

        response = requests.post(f"{BASE_URL}/users", json=data)

        # Проверка статус кода
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

        # Проверка структуры JSON
        json_data = response.json()
        expected_keys = ['id', 'name', 'username', 'email']
        for key in expected_keys:
            assert key in json_data, f"Missing key: {key}"

        # Проверка значений полей
        assert json_data['name'] == "John Doe"
        assert json_data['username'] == "johndoe"
        assert json_data['email'] == "john@example.com"
        assert isinstance(json_data['id'], int)

    def test_update_user(self):
        """Тест для PUT запроса - обновление пользователя"""
        data = {
            "id": 1,
            "name": "Updated Name",
            "username": "updateduser",
            "email": "updated@example.com"
        }

        response = requests.put(f"{BASE_URL}/users/1", json=data)

        # Проверка статус кода
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        # Проверка структуры JSON
        json_data = response.json()
        expected_keys = ['id', 'name', 'username', 'email']
        for key in expected_keys:
            assert key in json_data, f"Missing key: {key}"

        # Проверка значений полей
        assert json_data['name'] == "Updated Name"
        assert json_data['username'] == "updateduser"
        assert json_data['email'] == "updated@example.com"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])