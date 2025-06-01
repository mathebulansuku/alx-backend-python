#!/usr/bin/env python3
"""
Unit tests and integration tests for client.GithubOrgClient
"""
import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

class TestGithubOrgClient(unittest.TestCase):
    """Test suite for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org property"""
        test_payload = {"login": org_name, "id": 1234}
        mock_get_json.return_value = test_payload

        client_instance = GithubOrgClient(org_name)
        result = client_instance.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Unit-test _public_repos_url property."""
        test_payload = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
        with patch.object(GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("testorg")
            self.assertEqual(client._public_repos_url, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Unit-test GithubOrgClient.public_repos method."""
        test_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_repos_payload

        test_url = "http://test.url/api/repos"
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = test_url

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            # The method should return the list of repo names
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            # _public_repos_url property should be called once
            mock_url.assert_called_once()
            # get_json should be called once with the URL
            mock_get_json.assert_called_once_with(test_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Unit-test GithubOrgClient.has_license static method."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls):
        """Set up class-level mock for requests.get."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def get_json_side_effect(url):
            if url == f"https://api.github.com/orgs/{cls.org_payload['login']}":
                return Mock(json=Mock(return_value=cls.org_payload))
            if url == cls.org_payload["repos_url"]:
                return Mock(json=Mock(return_value=cls.repos_payload))
            return Mock(json=Mock(return_value=None))

        cls.mock_get.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop class-level patch."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos."""
        client = GithubOrgClient(self.org_payload['login'])
        self.assertEqual(client.public_repos(), self.expected_repos)

if __name__ == '__main__':
    unittest.main()
