# ALX Backend Python: Unittests and Integration Tests

This project demonstrates best practices in Python unit testing and integration testing, following the ALX curriculum for backend development.

## 📂 Project Structure

- `utils.py`: Utility functions and decorators for API work and memoization.
- `client.py`: `GithubOrgClient` class for interacting with the GitHub API.
- `fixtures.py`: Contains JSON-like payloads for integration tests.
- `test_utils.py`: Unit tests for the `utils.py` functions.
- `test_client.py`: Unit and integration tests for `client.py`.

---

## 🧪 Running the Tests

To run all tests, use:

```bash
python3 -m unittest test_utils.py
python3 -m unittest test_client.py
```
