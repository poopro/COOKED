from flask import request

from ..config import Config


HEADER_TO_CONFIG = {
    "X-LLM-API-Key": "LLM_API_KEY",
    "X-LLM-Base-URL": "LLM_BASE_URL",
    "X-LLM-Model": "LLM_MODEL_NAME",
    "X-ZEP-API-Key": "ZEP_API_KEY",
}


def apply_demo_key_overrides():
    """Apply local-demo API keys sent by the UI for this request.

    The values are only held in the Flask process memory and are never written
    to project files. This keeps local demos convenient without committing keys.
    """
    for header, config_attr in HEADER_TO_CONFIG.items():
        value = request.headers.get(header)
        if value and value.strip():
            setattr(Config, config_attr, value.strip())
