import numpy as np
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


def test_play_audio_array():
    audio = np.zeros(1000, dtype=np.float32)
    with patch("sounddevice.play") as mock_play, patch("sounddevice.wait") as mock_wait:
        from kitten_cli.playback import play_audio_array
        play_audio_array(audio, 24000)
        mock_play.assert_called_once_with(audio, samplerate=24000)
        mock_wait.assert_called_once()


def test_play_audio(tmp_path):
    audio = np.zeros(1000, dtype=np.float32)
    wav_path = tmp_path / "test.wav"

    with patch("soundfile.read", return_value=(audio, 24000)) as mock_read, \
         patch("sounddevice.play"), \
         patch("sounddevice.wait"):
        from kitten_cli.playback import play_audio
        play_audio(wav_path)
        mock_read.assert_called_once_with(str(wav_path))
