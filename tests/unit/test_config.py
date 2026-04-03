import os
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.utils.config import load_config, load_test_data, load_yaml, resolve_env_var


class TestConfigUtils:
    def test_resolve_env_var_no_env(self):
        result = resolve_env_var("plain_text")
        assert result == "plain_text"

    @patch.dict(os.environ, {"TEST_VAR": "test_value"})
    def test_resolve_env_var_with_env(self):
        result = resolve_env_var("${ENV:TEST_VAR}")
        assert result == "test_value"

    @patch.dict(os.environ, {"TEST_VAR": ""})
    def test_resolve_env_var_empty_env(self):
        result = resolve_env_var("${ENV:TEST_VAR}")
        assert result == ""

    def test_resolve_env_var_missing_env(self):
        result = resolve_env_var("${ENV:NONEXISTENT}")
        assert result == ""

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="key: value\nlist:\n  - item1\n  - item2",
    )
    def test_load_yaml(self, mock_file):
        result = load_yaml("test.yaml")
        assert result == {"key": "value", "list": ["item1", "item2"]}

    @patch("pathlib.Path.exists")
    @patch("src.utils.config.load_yaml")
    def test_load_config_env_specific(self, mock_load_yaml, mock_exists):
        mock_exists.return_value = True
        mock_load_yaml.return_value = {"env": "test"}

        result = load_config("test")
        assert result == {"env": "test"}

    @patch("pathlib.Path.exists")
    @patch("src.utils.config.load_yaml")
    def test_load_test_data(self, mock_load_yaml, mock_exists):
        mock_exists.return_value = True
        mock_load_yaml.return_value = {"username": "test"}

        result = load_test_data("login/test.yaml")
        assert result == {"username": "test"}
