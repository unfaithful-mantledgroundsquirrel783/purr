from pathlib import Path

import sounddevice as sd
import soundfile as sf


def play_audio_array(audio, sample_rate: int) -> None:
    sd.play(audio, samplerate=sample_rate)
    sd.wait()


def play_audio(path: Path) -> None:
    audio, sample_rate = sf.read(str(path))
    play_audio_array(audio, sample_rate)
