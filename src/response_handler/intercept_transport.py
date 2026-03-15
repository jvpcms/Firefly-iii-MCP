import httpx
import json
import os
from uuid import uuid4, UUID

from config import env_config


class InterceptingTransport(httpx.AsyncBaseTransport):
    """Intercept tools response and save the data to .json files.

    This is done to allow claude to filter only relevant fields,
    saving context tokens."""

    def __init__(self, wrapped: httpx.AsyncBaseTransport):
        self._wrapped = wrapped
        self._save_path = env_config.tool_data_path
        os.makedirs(self._save_path, exist_ok=True)

    def _save_json_tool_data(self, data: dict) -> UUID:
        file_id = uuid4()
        file_path = os.path.join(self._save_path, f"{file_id}.json")
        with open(file_path, "w") as f:
            json.dump(data, f)

        return file_id

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        response = await self._wrapped.handle_async_request(request)
        body = await response.aread()

        try:
            data = json.loads(body)
            file_id = self._save_json_tool_data(data)
            body = json.dumps({"result": "success", "data_id": str(file_id)}).encode()
        except Exception:
            pass  # leave non-JSON responses untouched

        return httpx.Response(
            status_code=response.status_code,
            headers=response.headers,
            content=body,
        )
