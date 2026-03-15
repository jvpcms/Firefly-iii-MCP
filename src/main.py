import os
import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP

from routes import semantic_maps, register_custom_routes
from spec import load_openapi_spec

load_dotenv()

client = httpx.AsyncClient(
    base_url=os.environ["FIREFLY_III_URL"],
    headers={"Authorization": "Bearer " + os.environ["FIREFLY_III_ACCESS_TOKEN"]},
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
