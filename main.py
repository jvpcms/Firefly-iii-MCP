import os
import yaml
import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.experimental.server.openapi import RouteMap, MCPType
from starlette.responses import JSONResponse

load_dotenv()
with open("./firefly-iii-openapi.yaml", "r") as f:
    openapi_spec = yaml.safe_load(f)

import re as _re

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

# Claude Code treats 'application/vnd.api+json' as binary and saves it to a file.
# Replace with 'application/json' so responses are returned as inline text.
def _replace_mime(obj):
    if isinstance(obj, dict):
        return {
            ("application/json" if k == "application/vnd.api+json" else k): _replace_mime(v)
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [_replace_mime(i) for i in obj]
    return obj
openapi_spec = _replace_mime(openapi_spec)

client = httpx.AsyncClient(
    base_url=os.environ["FIREFLY_III_URL"],
    headers={"Authorization": "Bearer " + os.environ["FIREFLY_III_ACCESS_TOKEN"]},
)

semantic_maps = [
    RouteMap(methods="*", pattern=r"^/v1/about.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(methods="*", pattern=r"^/v1/autocomplete.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(methods="*", pattern=r"^/v1/configuration.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(methods="*", pattern=r"^/v1/preferences.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(methods="*", pattern=r"^/v1/webhooks.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(methods="*", pattern=r"^/v1/user-groups.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(methods="*", pattern=r"^/v1/users.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(methods="*", pattern=r"^/v1/tags.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(methods="*", pattern=r"^/v1/search.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(methods="*", pattern=r"^/v1/rules.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(methods="*", pattern=r"^/v1/recurrences.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(methods="*", pattern=r"^/v1/rules-groups.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(methods="*", pattern=r"^/v1/links.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(methods="*", pattern=r"^/v1/data.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(methods="*", pattern=r"^/v1/currencies.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(methods="*", pattern=r"^/v1/exchange-rates.*", mcp_type=MCPType.EXCLUDE),
    RouteMap(
        methods=["GET"], pattern=r"^/v1/summary/basic$", mcp_type=MCPType.RESOURCE
    ),
    RouteMap(methods=["GET"], pattern=r"^/v1/accounts$", mcp_type=MCPType.TOOL),
    RouteMap(methods=["GET"], pattern=r"^/v1/attachments$", mcp_type=MCPType.RESOURCE),
    RouteMap(
        methods=["GET"], pattern=r"^/v1/available-budgets$", mcp_type=MCPType.RESOURCE
    ),
    RouteMap(methods=["GET"], pattern=r"^/v1/bills$", mcp_type=MCPType.RESOURCE),
    RouteMap(methods=["GET"], pattern=r"^/v1/budgets$", mcp_type=MCPType.RESOURCE),
    RouteMap(methods=["GET"], pattern=r"^/v1/categories$", mcp_type=MCPType.RESOURCE),
    RouteMap(methods=["GET"], pattern=r"^/v1/data$", mcp_type=MCPType.RESOURCE),
    RouteMap(methods=["GET"], pattern=r"^/v1/piggy-banks$", mcp_type=MCPType.RESOURCE),
    RouteMap(methods=["GET"], pattern=r"^/v1/transactions$", mcp_type=MCPType.TOOL),
    RouteMap(
        methods=["GET"],
        pattern=r"^/v1/accounts/{id}",
        mcp_type=MCPType.RESOURCE_TEMPLATE,
    ),
    RouteMap(
        methods=["GET"],
        pattern=r"^/v1/piggy-banks/{id}",
        mcp_type=MCPType.RESOURCE_TEMPLATE,
    ),
    RouteMap(
        methods=["GET"],
        pattern=r"^/v1/object-groups/{id}",
        mcp_type=MCPType.RESOURCE_TEMPLATE,
    ),
    RouteMap(methods=["POST"], pattern=r"^/v1/accounts", mcp_type=MCPType.TOOL),
    RouteMap(methods=["POST"], pattern=r"^/v1/transactions", mcp_type=MCPType.TOOL),
    RouteMap(methods=["POST"], pattern=r"^/v1/budgets", mcp_type=MCPType.TOOL),
    RouteMap(methods=["POST"], pattern=r"^/v1/attachments", mcp_type=MCPType.TOOL),
    RouteMap(methods=["POST"], pattern=r"^/v1/bills", mcp_type=MCPType.TOOL),
    RouteMap(methods=["POST"], pattern=r"^/v1/categories", mcp_type=MCPType.TOOL),
]

mcp = FastMCP.from_openapi(
    name="Firefly III MCP server",
    openapi_spec=openapi_spec,
    client=client,
    route_maps=semantic_maps,
    validate_output=False,
)
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    """
    Health check endpoint to verify the server is running.
    """
    return  JSONResponse({"status": "ok", "service": "Firefly III MCP"})

@mcp.prompt
def get_account_balance_prompt(account_name: str) -> str:
    """
    Generates a prompt to get the current balance of a specified account.
    """
    return f"What is the current balance of the account named '{account_name}'?"


@mcp.prompt
def summarize_spending_by_category_prompt(start_date: str, end_date: str) -> str:
    """
    Generates a prompt to summarize spending by category within a date range (YYYY-MM-DD).
    """
    return f"Please provide a summary of my spending by category from {start_date} to {end_date}."

app = mcp.http_app()
