import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


def test_is_model_downloaded_false(tmp_path):
    from kitten_cli import config
    with patch.object(config, "MODELS_DIR", tmp_path):
        from kitten_cli.models import is_model_downloaded
        assert not is_model_downloaded("nano")


def test_is_model_downloaded_true(tmp_path):
    model_dir = tmp_path / "nano"
    model_dir.mkdir()
    (model_dir / "model.onnx").write_bytes(b"fake")

    from kitten_cli import config
    with patch.object(config, "MODELS_DIR", tmp_path):
        from kitten_cli.models import is_model_downloaded
        assert is_model_downloaded("nano")


def test_remove_model_unknown(tmp_path):
    import typer
    from kitten_cli import config
    with patch.object(config, "MODELS_DIR", tmp_path):
        from kitten_cli.models import remove_model
        with pytest.raises(SystemExit):
            remove_model("nonexistent")


def test_remove_model_not_installed(tmp_path):
    import typer
    from kitten_cli import config
    with patch.object(config, "MODELS_DIR", tmp_path):
        from kitten_cli.models import remove_model
        with pytest.raises(SystemExit):
            remove_model("nano")


def test_remove_model_success(tmp_path):
    model_dir = tmp_path / "nano"
    model_dir.mkdir()
    (model_dir / "model.onnx").write_bytes(b"fake")

    from kitten_cli import config
    with patch.object(config, "MODELS_DIR", tmp_path):
        from kitten_cli.models import remove_model
        remove_model("nano")
    assert not model_dir.exists()


def test_ensure_kittentts_missing():
    import builtins
    real_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name == "kittentts":
            raise ImportError("no module")
        return real_import(name, *args, **kwargs)

    with patch("builtins.__import__", side_effect=mock_import):
        from kitten_cli.models import _ensure_kittentts
        with pytest.raises(SystemExit):
            _ensure_kittentts()
