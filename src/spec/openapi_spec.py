from typing import Any
from pathlib import Path
import yaml
import re as _re

_SPEC_PATH = Path(__file__).parent.parent.parent / "firefly-iii-openapi.yaml"


def load_openapi_spec() -> dict[str, Any]:
    """Load and sanitize openApi spec at the default path"""

    openapi_spec: dict[str, Any] | None = None
    with open(_SPEC_PATH, "r") as f:
        openapi_spec = yaml.safe_load(f)

    if openapi_spec is None:
        raise Exception("Failed to load openApi spec.")

    # Claude API requires property keys to match '^[a-zA-Z0-9_.-]{1,64}'.
    # The Firefly OpenAPI spec uses names like 'accounts[]', 'tags[]', etc.
    # Strip the trailing '[]' from all parameter names to make them valid.
    _INVALID_SUFFIX = _re.compile(r'\[\]$')
    for _path_item in openapi_spec.get("paths", {}).values():
        for _op in _path_item.values():
            if not isinstance(_op, dict):
                continue
            for _param in _op.get("parameters", []):
                if "name" in _param:
                    _param["name"] = _INVALID_SUFFIX.sub("", _param["name"])

    return openapi_spec
