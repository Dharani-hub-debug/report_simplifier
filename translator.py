import json
import os
import time

from dotenv import load_dotenv

load_dotenv()

CACHE_FILE = "translation_cache.json"
LANGUAGE_NAMES = {"hi": "Hindi", "kn": "Kannada"}
MODEL = "gemini-flash-latest"
BACKUP_MODEL = "gemini-flash-lite-latest"

_client = None


def _get_client():
    global _client
    if _client is None:
        from google import genai

        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client


def _load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def translate(text, lang):
    """Returns the translated text, or None if the API could not do it."""
    if lang not in LANGUAGE_NAMES:
        return None

    cache = _load_cache()
    key = f"{lang}|{text}"
    if key in cache:
        return cache[key]

    prompt = (
        f"Translate the sentence below into {LANGUAGE_NAMES[lang]}, using very simple "
        "everyday words that a person with no medical knowledge can understand. "
        "Do not add or remove any information and do not give advice. "
        "Reply with only the translation.\n\n" + text
    )
    for model in (MODEL, BACKUP_MODEL):
        try:
            response = _get_client().models.generate_content(model=model, contents=prompt)
            result = response.text.strip()
            if result:
                cache[key] = result
                _save_cache(cache)
                return result
        except Exception:
            time.sleep(1)
    return None