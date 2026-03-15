from fastmcp.experimental.server.openapi import RouteMap, MCPType

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
