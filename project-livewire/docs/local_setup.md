# Project Livewire - Local Setup Guide

This guide provides detailed instructions for setting up and running Project Livewire on your local machine for development and testing.

## Prerequisites

Before you begin, ensure you have the following installed and configured:

1.  **Python:** Version 3.8 or higher. ([Download](https://www.python.org/downloads/))
2.  **pip:** Python package installer (usually included with Python).
3.  **Git:** For cloning the repository. ([Download](https://git-scm.com/))
4.  **API Keys:**
    *   **Google Gemini API Key:** Required for interacting with the Gemini model.
        *   Get one from [Google AI Studio](https://makersuite.google.com/app/apikey).

## Setup Steps

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/heiko-hotz/project-livewire.git
    cd project-livewire
    ```

2.  **Backend Configuration (`.env` file):**
    *   Navigate to the server directory:
        ```bash
        cd server
        ```
    *   Create the `.env` file:
        ```bash
        echo "GOOGLE_API_KEY=your_api_key_here" > .env
        ```
    *   Replace `your_api_key_here` with your actual Google Gemini API key.

3.  **Install Backend Dependencies:**
    *   Make sure you are still in the `server/` directory.
    *   (Optional but recommended) Create and activate a virtual environment:
        ```bash
        python3 -m venv venv
        source venv/bin/activate # Linux/macOS
        # venv\Scripts\activate # Windows
        ```
    *   Install required packages:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Start the Backend Server:**
    *   While in the `server/` directory:
        ```bash
        python server.py
        ```
    *   The server will start, usually listening on `0.0.0.0:8081`. Look for the log message `Running websocket server on 0.0.0.0:8081...`. Keep this terminal running.

5.  **Start the Frontend Server:**
    *   Open a **new terminal window/tab**.
    *   Navigate to the client directory:
        ```bash
        cd ../client # Or navigate from the project root: cd project-livewire/client
        ```
    *   Start a simple Python HTTP server:
        ```bash
        python -m http.server 8000
        ```
    *   This server serves the HTML, CSS, and JavaScript files. Keep this terminal running.

6.  **Access the Application:**
    *   Open your web browser.
    *   Navigate to the **Development UI:** `http://localhost:8000/index.html`
    *   Or navigate to the **Mobile UI:** `http://localhost:8000/mobile.html`

## Testing the Connection

1.  Open your browser's developer console (usually F12).
2.  Check the "Console" tab for any errors, especially WebSocket connection errors.
3.  Look for a "WebSocket connection established" or similar message from the client-side JavaScript.
4.  Try clicking the microphone button (or play button on mobile) and speaking, or typing a message in the text input (dev UI).
5.  Observe the terminal running the `server.py` script for log messages indicating client connections and messages being processed.

## Troubleshooting

*   **`Connection refused` errors (WebSocket):**
    *   Ensure the backend server (`server.py`) is running in the other terminal.
    *   Verify the WebSocket URL in the client JavaScript (`client/src/api/gemini-api.js`) matches where the server is listening (default `ws://localhost:8081`).
*   **`ModuleNotFoundError`:** Make sure you installed dependencies using `pip install -r requirements.txt` in the `server/` directory (and activated your virtual environment if you created one).
*   **API Key Errors / Authentication Errors:**
    *   Double-check the `GOOGLE_API_KEY` in your `.env` file.
    *   Check server logs for specific authentication failure messages.
*   **Port Conflicts:** If `8081` or `8000` are already in use, the servers might fail to start. Stop the conflicting process or configure the servers/client to use different ports (requires code changes).
*   **Microphone/Webcam Access Denied:** Ensure you grant permission in your browser when prompted. Check browser settings if you previously denied access.