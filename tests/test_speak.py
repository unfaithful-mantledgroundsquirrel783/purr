import numpy as np
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


def _make_fake_kittentts():
    mock_tts = MagicMock()
    mock_tts.synthesize.return_value = np.zeros(24000, dtype=np.float32)
    mock_class = MagicMock(return_value=mock_tts)
    return mock_class, mock_tts


def test_synthesize_writes_file(tmp_path):
    mock_class, mock_tts = _make_fake_kittentts()
    output = tmp_path / "out.wav"

    with (
        patch("kitten_cli.speak._ensure_kittentts"),
        patch("kitten_cli.speak.is_model_downloaded", return_value=True),
        patch.dict("sys.modules", {"kittentts": MagicMock(KittenTTS=mock_class)}),
    ):
        from kitten_cli import speak as speak_mod
        with patch.object(speak_mod, "KittenTTS" if hasattr(speak_mod, "KittenTTS") else "_ensure_kittentts", create=True):
            pass

        import importlib
        import kitten_cli.speak
        importlib.reload(kitten_cli.speak)

        with patch("kitten_cli.speak._ensure_kittentts"), \
             patch("kitten_cli.speak.is_model_downloaded", return_value=True), \
             patch("kitten_cli.speak.install_model"), \
             patch("soundfile.write") as mock_sf_write:

            import kittentts as _kt
            _kt.KittenTTS = mock_class

            result = kitten_cli.speak.synthesize(
                "Hello world",
                model="nano",
                output=output,
                play=False,
            )
            mock_sf_write.assert_called_once()
            assert result == output


def test_synthesize_unknown_model():
    with patch("kitten_cli.speak._ensure_kittentts"):
        from kitten_cli.speak import synthesize
        with pytest.raises(SystemExit):
            synthesize("hi", model="unknown-model", output=Path("/tmp/x.wav"))
