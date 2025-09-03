import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from typing import List, Dict, Any
from db import CloudDB  # Импортируйте ваш реальный модуль

# Фикстуры для тестов
@pytest.fixture
def cloud_db():
    """Создает экземпляр CloudDB для тестирования"""
    return CloudDB()

@pytest.fixture
def sample_data():
    """Пример данных для тестирования"""
    return {
        "name": "Test Task",
        "status": "pending",
        "description": "Test description"
    }

@pytest.fixture
def mock_response():
    """Мок ответа от API"""
    def create_mock_response(json_data, status_code=200):
        mock = Mock()
        mock.json.return_value = json_data
        mock.status_code = status_code
        mock.raise_for_status = Mock()
        return mock
    return create_mock_response

# Тесты для CloudDB
class TestCloudDB:

    @patch('db.requests.get')
    def test_get_json_success(self, mock_get, cloud_db, mock_response):
        """Тест успешного получения JSON из облака"""
        # Мокируем ответ API
        test_data = {"1": {"name": "test"}, "2": {"name": "test2"}}
        mock_get.return_value = mock_response(test_data)
        
        result = cloud_db._CloudDB__get_json()
        
        assert result == test_data
        mock_get.assert_called_once_with(
            "https://api.jsonbin.io/v3/b/68b1c53ed0ea881f406a555a",
            headers={
                'X-Master-Key': '$2a$10$gkEEHNtdmq7FCAUiGF88k.IDmciahKhZmVL7ZBfbANA6US9nsQsu6',
                'X-Bin-Meta': 'false'
            }
        )

    @patch('db.requests.get')
    def test_get_json_failure(self, mock_get, cloud_db, mock_response):
        """Тест обработки ошибки при получении JSON"""
        mock_get.return_value = mock_response({}, 404)
        mock_get.return_value.raise_for_status.side_effect = Exception("API Error")
        
        with pytest.raises(Exception):
            cloud_db._CloudDB__get_json()

    @patch('db.requests.put')
    @patch('db.requests.get')
    def test_add_success(self, mock_get, mock_put, cloud_db, sample_data, mock_response):
        """Тест успешного добавления элемента"""
        # Мокируем начальные данные
        mock_get.return_value = mock_response({})
        mock_put.return_value = mock_response({}, 200)
        
        result = cloud_db.add(1, sample_data)
        
        assert result is True
        mock_put.assert_called_once()

    @patch('db.requests.get')
    def test_get_all(self, mock_get, cloud_db, mock_response):
        """Тест получения всех элементов"""
        test_data = {"1": {"name": "test1"}, "2": {"name": "test2"}}
        mock_get.return_value = mock_response(test_data)
        
        result = cloud_db.get_all()
        
        assert result == [{"name": "test1"}, {"name": "test2"}]
        assert len(result) == 2

    @patch('db.requests.get')
    def test_get_existing_item(self, mock_get, cloud_db, mock_response):
        """Тест получения существующего элемента"""
        test_data = {"1": {"name": "test1"}, "2": {"name": "test2"}}
        mock_get.return_value = mock_response(test_data)
        
        result = cloud_db.get(1)
        
        assert result == {"name": "test1"}

    @patch('db.requests.get')
    def test_get_nonexistent_item(self, mock_get, cloud_db, mock_response):
        """Тест получения несуществующего элемента"""
        test_data = {"1": {"name": "test1"}}
        mock_get.return_value = mock_response(test_data)
        
        result = cloud_db.get(999)
        
        assert result is None

    @patch('db.requests.put')
    @patch('db.requests.get')
    def test_delete_existing_item(self, mock_get, mock_put, cloud_db, mock_response):
        """Тест удаления существующего элемента"""
        test_data = {"1": {"name": "test1"}, "2": {"name": "test2"}}
        mock_get.return_value = mock_response(test_data)
        mock_put.return_value = mock_response({}, 200)
        
        result = cloud_db.delete(1)
        
        assert result is True
        mock_put.assert_called_once()

    @patch('db.requests.get')
    def test_delete_nonexistent_item(self, mock_get, cloud_db, mock_response):
        """Тест удаления несуществующего элемента"""
        test_data = {"1": {"name": "test1"}}
        mock_get.return_value = mock_response(test_data)
        
        result = cloud_db.delete(999)
        
        assert result is False

    @patch('db.requests.put')
    @patch('db.requests.get')
    def test_update_existing_item(self, mock_get, mock_put, cloud_db, mock_response, sample_data):
        """Тест обновления существующего элемента"""
        test_data = {"1": {"name": "old_name"}}
        mock_get.return_value = mock_response(test_data)
        mock_put.return_value = mock_response({}, 200)
        
        result = cloud_db.update(1, sample_data)
        
        assert result is True
        mock_put.assert_called_once()

    @patch('db.requests.get')
    def test_update_nonexistent_item(self, mock_get, cloud_db, mock_response, sample_data):
        """Тест обновления несуществующего элемента"""
        test_data = {"1": {"name": "test1"}}
        mock_get.return_value = mock_response(test_data)
        
        result = cloud_db.update(999, sample_data)
        
        assert result is False

    @patch('db.requests.put')
    @patch('db.requests.get')
    def test_add_multiple_items(self, mock_get, mock_put, cloud_db, sample_data, mock_response):
        """Тест добавления нескольких элементов"""
        mock_get.return_value = mock_response({})
        mock_put.return_value = mock_response({}, 200)
        
        # Добавляем несколько элементов
        cloud_db.add(1, sample_data)
        cloud_db.add(2, {"name": "second_task"})
        
        assert mock_put.call_count == 2

    @patch('db.requests.put')
    @patch('db.requests.get')
    def test_data_persistence_simulation(self, mock_get, mock_put, cloud_db, sample_data, mock_response):
        """Тест симуляции сохранения данных"""
        # Первый вызов - пустые данные
        mock_get.return_value = mock_response({})
        mock_put.return_value = mock_response({}, 200)
        
        cloud_db.add(1, sample_data)
        
        # Второй вызов - данные должны содержать добавленный элемент
        test_data_after_add = {"1": sample_data}
        mock_get.return_value = mock_response(test_data_after_add)
        
        result = cloud_db.get(1)
        assert result == sample_data

    @patch('db.requests.put')
    @patch('db.requests.get')
    def test_json_serialization(self, mock_get, mock_put, cloud_db, sample_data, mock_response):
        """Тест корректной сериализации JSON"""
        mock_get.return_value = mock_response({})
        mock_put.return_value = mock_response({}, 200)
        
        cloud_db.add(1, sample_data)
        
        # Проверяем, что put был вызван с правильными данными
        call_args = mock_put.call_args
        assert call_args is not None
        # Проверяем, что данные были сериализованы в JSON
        assert '"name": "Test Task"' in call_args[1]['data']

# Тесты для обработки ошибок
class TestCloudDBErrorHandling:

    @patch('db.requests.get')
    def test_get_json_network_error(self, mock_get, cloud_db):
        """Тест обработки сетевой ошибки"""
        mock_get.side_effect = Exception("Network error")
        
        with pytest.raises(Exception):
            cloud_db._CloudDB__get_json()

    @patch('db.requests.put')
    @patch('db.requests.get')
    def test_add_network_error(self, mock_get, mock_put, cloud_db, sample_data, mock_response):
        """Тест обработки сетевой ошибки при добавлении"""
        mock_get.return_value = mock_response({})
        mock_put.side_effect = Exception("Network error")
        
        with pytest.raises(Exception):
            cloud_db.add(1, sample_data)

# Запуск тестов
if __name__ == "__main__":
    pytest.main([__file__, "-v"])