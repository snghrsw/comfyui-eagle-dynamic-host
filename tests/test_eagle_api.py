import importlib.util
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# ルートの __init__.py を経由せずに api/eagle_api.py を直接ロードする
_eagle_api_path = Path(__file__).resolve().parents[1] / "api" / "eagle_api.py"
_spec = importlib.util.spec_from_file_location("eagle_api", _eagle_api_path)
eagle_api_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(eagle_api_mod)

EagleAPI = eagle_api_mod.EagleAPI
FILE_SERVER_PORT = eagle_api_mod.FILE_SERVER_PORT


class TestAddFromUrl(unittest.TestCase):
    def setUp(self):
        self.api = EagleAPI.__new__(EagleAPI)
        self.api.base_url = "http://localhost:41595/api"
        self.api.token = "test-token"

    @patch.object(eagle_api_mod.requests, "post")
    def test_uses_custom_host(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200)

        self.api.add_from_url("test.png", ["tag1"], "folder1", file_server_host="hira-win")

        called_json = mock_post.call_args[1]["json"]
        self.assertEqual(called_json["url"], f"http://hira-win:{FILE_SERVER_PORT}/test.png")

    @patch.object(eagle_api_mod.requests, "post")
    def test_uses_default_localhost(self, mock_post):
        mock_post.return_value = MagicMock(status_code=200)

        self.api.add_from_url("test.png", ["tag1"], "folder1")

        called_json = mock_post.call_args[1]["json"]
        self.assertEqual(called_json["url"], f"http://localhost:{FILE_SERVER_PORT}/test.png")


if __name__ == "__main__":
    unittest.main()
