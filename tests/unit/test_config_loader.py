import pytest
from unittest.mock import patch, mock_open

from language_tutor.agent.config_loader import get_node_config

MOCK_YAML = """
japanese_tutor:
  current_version: "v0.1.0"
  versions:
    v0.1.0:
      model: "gemini-3.1-flash-lite"
      temperature: 1.0
      prompt: |
        You are a japanese tutor.
"""

MOCK_YAML_NO_TEMP = """
japanese_tutor:
  current_version: "v0.1.0"
  versions:
    v0.1.0:
      model: "gemini-3.1-flash-lite"
      prompt: |
        You are a japanese tutor.
"""


@patch("builtins.open", new_callable=mock_open, read_data=MOCK_YAML)
def test_get_node_config_success(mock_file):
    """
    Tests a basic example of reading a string of yaml and returning the dictionary
    """
    # Run command with intercepted yaml string
    model, prompt, temp = get_node_config("japanese_tutor", version="v0.1.0")

    # Assert values are as we expect
    assert model == "gemini-3.1-flash-lite"
    assert prompt == "You are a japanese tutor.\n"
    assert temp == 1.0


@patch("builtins.open", new_callable=mock_open, read_data=MOCK_YAML)
def test_get_node_config_no_version(mock_file):
    """
    Tests a basic example where node name is passed, but not a version
    """
    # Run command with intercepted yaml string
    model, prompt, temp = get_node_config("japanese_tutor")

    # Assert values are as we expect
    assert model == "gemini-3.1-flash-lite"
    assert prompt == "You are a japanese tutor.\n"
    assert temp == 1.0


@patch("builtins.open", new_callable=mock_open, read_data=MOCK_YAML_NO_TEMP)
def test_get_node_config_default_temperature(mock_file):
    """
    Tests that a default temperature is used if not provided in the config.
    """
    # Run command with intercepted yaml string
    model, prompt, temp = get_node_config("japanese_tutor")

    # Assert values are as we expect
    assert model == "gemini-3.1-flash-lite"
    assert prompt == "You are a japanese tutor.\n"
    assert temp == 1.0


@patch("builtins.open", new_callable=mock_open, read_data=MOCK_YAML)
def test_get_node_config_invalid_node_name(mock_file):
    """
    Test that a KeyError occurs if a non-existent node name is passed.
    """
    with pytest.raises(KeyError) as exc_info:
        get_node_config("incorrect_node_name", "v0.1.0")

    # Verify that the missing key name matches the incorrect input
    assert exc_info.value.args[0] == "incorrect_node_name"


@patch("builtins.open", new_callable=mock_open, read_data=MOCK_YAML)
def test_get_node_config_invalid_version(mock_file):
    """
    Test that a KeyError occurs if a non-existent version is passed.
    """
    with pytest.raises(KeyError) as exc_info:
        get_node_config("japanese_tutor", "v9.9.9")

    # Verify that the missing key name matches the incorrect input
    assert exc_info.value.args[0] == "v9.9.9"


@patch("builtins.open", new_callable=mock_open, read_data="BAD YAML TEXT")
def test_get_node_config_corrupt_yaml(mock_file):
    """
    Test handling of a non-yaml string being passed to the
    get_node_config function
    """
    with pytest.raises(TypeError):
        get_node_config("japanese_tutor")
