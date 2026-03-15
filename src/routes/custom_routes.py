import json
import os
from fastmcp import FastMCP
from starlette.responses import JSONResponse
from config import env_config

def register_custom_routes(mcp: FastMCP):
    """ Register custom routes to a mcp instance"""

    @mcp.tool()
    def load_tool_data(data_id: str) -> dict:
        """Load the full JSON response for a previous tool call by its data_id."""
        file_path = os.path.join(env_config.tool_data_path, f"{data_id}.json")
        with open(file_path, "r") as f:
            return json.load(f)

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
