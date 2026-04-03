"""
Tool registry for dispatching function calls to their implementations.
"""

import logging

from tools import maps_api

logger = logging.getLogger(__name__)

TOOL_HANDLERS = {
    "compute_route": maps_api.compute_route,
    "search_places_along_route": maps_api.search_places_along_route,
    "search_nearby_places": maps_api.search_nearby_places,
}


async def execute_tool(function_name: str, args: dict) -> dict:
    """Execute a tool by name with the given arguments.

    Args:
        function_name: The name of the function to execute.
        args: The arguments to pass to the function.

    Returns:
        The result dict from the tool execution.
    """
    handler = TOOL_HANDLERS.get(function_name)
    if not handler:
        logger.warning(f"Unknown function called: {function_name}")
        return {"error": f"Unknown function: {function_name}"}

    logger.info(f"Executing tool: {function_name} with args: {args}")
    try:
        result = await handler(**args)
        logger.info(f"Tool {function_name} completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error executing tool {function_name}: {e}")
        return {"error": f"Tool execution failed: {str(e)}"}
