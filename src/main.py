import httpx
from fastmcp import FastMCP

from config import env_config
from routes import semantic_maps, register_custom_routes
from spec import load_openapi_spec
from response_handler import InterceptingTransport

client = httpx.AsyncClient(
    base_url=env_config.firefly_iii_url,
    headers={"Authorization": "Bearer " + env_config.firefly_iii_access_token},
    transport=InterceptingTransport(httpx.AsyncHTTPTransport()),
)

openapi_spec = load_openapi_spec()

mcp = FastMCP.from_openapi(
    name="Firefly III MCP server",
    openapi_spec=openapi_spec,
    client=client,
    route_maps=semantic_maps,
    validate_output=False,
)

register_custom_routes(mcp)

app = mcp.http_app()
