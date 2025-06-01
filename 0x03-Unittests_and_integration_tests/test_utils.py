#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch, Mock

class TestAccessNestedMap(unittest.TestCase):
    """Test suite for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, missing_key):
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{missing_key}'")


if __name__ == '__main__':
    unittest.main()


class TestGetJson(unittest.TestCase):
    """Test suite for get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        # Arrange: set up the mock to return the payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Act: call the function
        result = get_json(test_url)

        # Assert: requests.get was called once with test_url
        mock_get.assert_called_once_with(test_url)
        # Assert: the result matches the test_payload
        self.assertEqual(result, test_payload)

        class TestMemoize(unittest.TestCase):
    """Test memoize decorator"""

    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()