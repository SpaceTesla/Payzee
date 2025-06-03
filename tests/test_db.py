from unittest.mock import patch
from db.redis_operations import (
    get_document,
    set_document,
    delete_document,
    get_all_documents,
    query_by_field,
    update_document,
    array_union,
)


class TestRedisOperations:
    def test_get_document_success(self, mock_redis):
        # Setup mock
        mock_redis.get.return_value = (
            b'{"name": "Test User", "email": "test@example.com"}'
        )

        # Call the function
        result = get_document("user:", "123")

        # Assertions
        assert result == {"name": "Test User", "email": "test@example.com"}
        mock_redis.get.assert_called_once_with("user:123")

    def test_get_document_not_found(self, mock_redis):
        # Setup mock
        mock_redis.get.return_value = None

        # Call the function
        result = get_document("user:", "non-existent")

        # Assertions
        assert result is None
        mock_redis.get.assert_called_once_with("user:non-existent")

    def test_set_document_without_index(self, mock_redis):
        # Test data
        test_data = {"name": "Test User", "email": "test@example.com"}

        # Call the function
        result = set_document("user:", "123", test_data)

        # Assertions
        assert result == "123"
        mock_redis.set.assert_called_once()

    def test_set_document_with_index(self, mock_redis):
        # Test data
        test_data = {"name": "Test User", "email": "test@example.com"}

        # Call the function
        result = set_document("user:", "123", test_data, index_set="users")

        # Assertions
        assert result == "123"
        mock_redis.set.assert_called_once()
        mock_redis.sadd.assert_called_once_with("users", "123")

    def test_delete_document(self, mock_redis):
        # Call the function
        result = delete_document("user:", "123", index_set="users")

        # Assertions
        assert result is True
        mock_redis.delete.assert_called_once_with("user:123")
        mock_redis.srem.assert_called_once_with("users", "123")

    def test_get_all_documents(self, mock_redis):
        # Setup mock
        mock_redis.smembers.return_value = ["1", "2"]

        # Mock the get_document function within the module
        with patch("db.redis_operations.get_document") as mock_get:
            mock_get.side_effect = [
                {"id": "1", "name": "User 1"},
                {"id": "2", "name": "User 2"},
            ]

            # Call the function
            result = get_all_documents("user:", "users")

            # Assertions
            assert len(result) == 2
            assert result[0]["name"] == "User 1"
            assert result[1]["name"] == "User 2"
            mock_redis.smembers.assert_called_once_with("users")

    def test_query_by_field_simple(self, mock_redis):
        # Setup mock
        mock_redis.smembers.return_value = ["1", "2", "3"]

        # Mock the get_document function within the module
        with patch("db.redis_operations.get_document") as mock_get:
            mock_get.side_effect = [
                {"name": "Areeb", "status": "active"},
                {"name": "Shivansh", "status": "inactive"},
                {"name": "Alfiya", "status": "active"},
            ]

            # Call the function
            result = query_by_field("user:", "users", "status", "active")

            # Assertions
            assert len(result) == 2
            assert result[0]["name"] == "Areeb"
            assert result[1]["name"] == "Alfiya"

    def test_query_by_field_nested(self, mock_redis):
        # Setup mock
        mock_redis.smembers.return_value = ["1", "2"]

        # Mock the get_document function within the module
        with patch("db.redis_operations.get_document") as mock_get:
            mock_get.side_effect = [
                {"account": {"level": "premium", "verified": True}},
                {"account": {"level": "basic", "verified": True}},
            ]

            # Call the function
            result = query_by_field("user:", "users", "account.level", "premium")

            # Assertions
            assert len(result) == 1
            assert result[0]["account"]["level"] == "premium"

    def test_update_document_success(self, mock_redis):
        # Test data
        existing_data = {"name": "Old Name", "email": "old@example.com"}
        update_data = {"name": "New Name"}

        # Mock the get_document function within the module
        with (
            patch("db.redis_operations.get_document", return_value=existing_data),
            patch("db.redis_operations.set_document") as mock_set,
        ):
            # Call the function
            result = update_document("user:", "123", update_data)

            # Assertions
            assert result is True
            expected_updated_data = {"name": "New Name", "email": "old@example.com"}
            mock_set.assert_called_once_with("user:", "123", expected_updated_data)

    def test_array_union(self, mock_redis):
        # Test data
        existing_data = {"tags": ["python", "redis"]}

        # Mock the get_document function within the module
        with (
            patch("db.redis_operations.get_document", return_value=existing_data),
            patch("db.redis_operations.set_document") as mock_set,
        ):
            # Call the function
            result = array_union("user:", "123", "tags", ["redis", "database"])

            # Assertions
            assert result is True
            expected_updated_data = {"tags": ["python", "redis", "database"]}
            mock_set.assert_called_once_with("user:", "123", expected_updated_data)
