import unittest
from unittest.mock import patch
import requests
import os
from main import get_repos, get_user, main

class TestGetRepos(unittest.TestCase):

    @patch('requests.get')
    def test_get_repos_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {'id': 1, 'name': 'repo1', 'svn_url': 'http://example.com/repo1'},
            {'id': 2, 'name': 'repo2', 'svn_url': 'http://example.com/repo2'}
        ]
        user = 'testuser'
        expected_result = (
            "  ID: 1\n"
            "  Nome: repo1\n"
            "  url: http://example.com/repo1\n"
            "  ID: 2\n"
            "  Nome: repo2\n"
            "  url: http://example.com/repo2\n"
        )
        result = get_repos(user)
        self.assertEqual(result, expected_result)

    @patch('requests.get')
    def test_get_repos_error(self, mock_get):
        mock_get.side_effect = Exception('Request failed')
        user = 'testuser'
        result = get_repos(user)
        self.assertIsInstance(result, Exception)
        self.assertEqual(str(result), 'Request failed')

class TestGetUser(unittest.TestCase):
    def test_successful_request(self):
        with patch('main.requests.get') as mock_get:
            mock_get.return_value.json.return_value = {'name': 'John Doe'}
            result = get_user()
            self.assertEqual(result, {'name': 'John Doe'})
            mock_get.assert_called_once_with(url='https://api.github.com/user', headers={'Authorization': f'Bearer {os.getenv("TOKEN")}'})

    def test_request_exception(self):
        with patch('main.requests.get') as mock_get:
            mock_get.side_effect = Exception('Request error')
            result = get_user()
            self.assertIsInstance(result, Exception)
            mock_get.assert_called_once_with(url='https://api.github.com/user', headers={'Authorization': f'Bearer {os.getenv("TOKEN")}'})

class UnitTestMain(unittest.TestCase):

    @patch('main.get_user')
    @patch('main.get_repos')
    def test_main(self, mock_get_repos, mock_get_user):
        # Mocking the return values of get_user and get_repos
        mock_get_user.return_value = {'name': 'John Doe', 'login': 'johndoe', 'public_repos': 5, 'followers': 10, 'following': 5}
        mock_get_repos.return_value = 'repo1\nrepo2\nrepo3'

        # Calling the main function
        main()

        # Asserting that the file was created with the correct content
        with open('johndoe.txt', 'r') as file:
            self.assertEqual(file.read(), 'Nome: John Doe\nPerfil: johndoe\nNúmero de repositórios publicos: 5\nNúmero de seguidores: 10\nNúmero de usuários seguidos: 5\nLista da Repositórios:\nrepo1\nrepo2\nrepo3')
        os.remove('johndoe.txt')

class APITestGetRepos(unittest.TestCase):

    def test_api_repos_success(self):
        response = requests.get("https://api.github.com/users/Kenjinh/repos")
        self.assertEqual(response.status_code, 200)
        repos = response.json()
        self.assertIsInstance(repos, list)
        for repo in repos:
            self.assertIsInstance(repo, dict)
            self.assertIn('id', repo)
            self.assertIn('name', repo)
            self.assertIn('svn_url', repo)

    def test_api_repos_error(self):
        response = requests.get("https://api.github.com/users/Kenjinhr/repos")
        self.assertNotEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

class APITestGetUser(unittest.TestCase):

    def test_api_user_success(self):
        response = requests.get(url=f"{os.getenv('GITHUB_API_URL')}/user", headers={"Authorization": f"Bearer {os.getenv('TOKEN')}"})
        self.assertEqual(response.status_code, 200)
        user = response.json()
        self.assertIsInstance(user, dict)
        self.assertIn('name', user)
        self.assertIn('login', user)
        self.assertIn('public_repos', user)
        self.assertIn('followers', user)
        self.assertIn('following', user)

    def test_api_user_error(self):
        response = requests.get("https://api.github.com/user", headers={"Authorization": "Bearer token"})
        self.assertNotEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
if __name__ == '__main__':
    unittest.main()