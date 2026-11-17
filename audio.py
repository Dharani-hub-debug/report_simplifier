import hashlib
import os

from gtts import gTTS

AUDIO_FOLDER = "audio_cache"
SUPPORTED = {"en", "hi", "kn"}


def make_audio(text, lang):
    """Returns the path of an mp3 file, or None if audio could not be made."""
    if lang not in SUPPORTED or not text.strip():
        return None

    os.makedirs(AUDIO_FOLDER, exist_ok=True)
    name = hashlib.md5(f"{lang}|{text}".encode("utf-8")).hexdigest() + ".mp3"
    path = os.path.join(AUDIO_FOLDER, name)

    if os.path.exists(path):
        return path

    try:
        gTTS(text=text, lang=lang).save(path)
        return path
    except Exception:
        return None
