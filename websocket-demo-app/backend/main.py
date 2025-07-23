import asyncio
import json

import websockets
from websockets.legacy.protocol import WebSocketCommonProtocol
from websockets.legacy.server import WebSocketServerProtocol

HOST = "generativelanguage.googleapis.com"
SERVICE_URL = f"wss://{HOST}/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent"

DEBUG = False


async def proxy_task(
    client_websocket: WebSocketCommonProtocol, server_websocket: WebSocketCommonProtocol
) -> None:
    """
    Forwards messages from one WebSocket connection to another.

    Args:
        client_websocket: The WebSocket connection from which to receive messages.
        server_websocket: The WebSocket connection to which to send messages.
    """
    async for message in client_websocket:
        try:
            data = json.loads(message)
            if DEBUG:
                print("proxying: ", data)
            await server_websocket.send(json.dumps(data))
        except Exception as e:
            print(f"Error processing message: {e}")

    await server_websocket.close()


async def create_proxy(
    client_websocket: WebSocketCommonProtocol, api_key: str
) -> None:
    """
    Establishes a WebSocket connection to the server and creates two tasks for
    bidirectional message forwarding between the client and the server.

    Args:
        client_websocket: The WebSocket connection of the client.
        api_key: The API key for authentication with the Google AI Studio server.
    """

    # Google AI Studio requires API key as query parameter
    service_url_with_key = f"{SERVICE_URL}?key={api_key}"

    async with websockets.connect(service_url_with_key) as server_websocket:
        client_to_server_task = asyncio.create_task(
            proxy_task(client_websocket, server_websocket)
        )
        server_to_client_task = asyncio.create_task(
            proxy_task(server_websocket, client_websocket)
        )
        await asyncio.gather(client_to_server_task, server_to_client_task)


async def handle_client(client_websocket: WebSocketServerProtocol) -> None:
    """
    Handles a new client connection, expecting the first message to contain an API key.
    Establishes a proxy connection to the server upon successful authentication.

    Args:
        client_websocket: The WebSocket connection of the client.
    """
    print("New connection...")
    # Wait for the first message from the client
    auth_message = await asyncio.wait_for(client_websocket.recv(), timeout=5.0)
    auth_data = json.loads(auth_message)

    if "api_key" in auth_data:
        api_key = auth_data["api_key"]
    else:
        print("Error: API key not found in the first message.")
        await client_websocket.close(code=1008, reason="API key missing")
        return

    await create_proxy(client_websocket, api_key)


async def main() -> None:
    """
    Starts the WebSocket server and listens for incoming client connections.
    """
    async with websockets.serve(handle_client, "localhost", 8080):
        print("Running websocket server localhost:8080...")
        # Run forever
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
