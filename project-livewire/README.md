# Project Livewire 

**Talk to AI like never before! Project Livewire is a real-time, multimodal chat application showcasing the power of Gemini 2.0 Flash (experimental) Live API.**

Think "Star Trek computer" interaction – speak naturally, show your webcam, share your screen, and get instant, streamed audio responses. Livewire brings this futuristic experience to your devices today.

This project builds upon the concepts from the [Gemini Multimodal Live API Developer Guide](https://github.com/heiko-hotz/gemini-multimodal-live-dev-guide) with a focus on a more production-ready setup and enhanced features.

## ✨ Key Features

*   **🎤 Real-time Voice:** Natural, low-latency voice conversations.
*   **👁️ Multimodal Input:** Combines voice, text, webcam video, and screen sharing.
*   **🔊 Streamed Audio Output:** Hear responses instantly as they are generated.
*   **↩️ Interruptible:** Talk over the AI, just like a real conversation.
*   **🔍 Google Search:** Get real-time information with built-in Google Search.
*   **📱 Responsive UI:** Includes both a development interface and a mobile-optimized view.

<!-- Optional: Add a GIF/Video Demo Here -->
<!-- ![Demo GIF](assets/livewire-demo.gif) -->

## 🚀 Getting Started

**Prerequisites:**

*   Python 3.8+
*   Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

---

### 1. 💻 Run Locally

These are the basic steps. For more detailed instructions, see the **[Local Setup Guide](./docs/local_setup.md)**.

1.  **Clone the repo:**
    ```bash
    git clone https://github.com/heiko-hotz/project-livewire.git
    cd project-livewire
    ```

2.  **Configure Backend:**
    ```bash
    cd server
    echo "GOOGLE_API_KEY=your_api_key_here" > .env
    ```

3.  **Run Backend:**
    ```bash
    pip install -r requirements.txt
    python server.py
    # Backend runs on localhost:8081
    ```

4.  **Run Frontend (in a *new* terminal):**
    ```bash
    cd ../client
    python -m http.server 8000
    # Frontend served on localhost:8000
    ```

5.  **Access:**
    *   Dev UI: `http://localhost:8000/index.html`
    *   Mobile UI: `http://localhost:8000/mobile.html`


## 🏗️ Architecture Overview

Project Livewire consists of:

1.  **Client (`client/`):** Vanilla JS frontend handling UI, media capture, and WebSocket connection.
2.  **Server (`server/`):** Python WebSocket server proxying to Gemini and managing sessions.
3.  **Gemini API:** Google's multimodal AI model accessed via the Live API with Google Search grounding.

![Architecture Diagram](assets/architecture.png)
*(User -> Client -> Server -> Gemini API with Google Search -> Server -> Client -> User)*

## ❓ Troubleshooting

*   Check terminal output for errors. Ensure `GOOGLE_API_KEY` in `.env` is correct.
*   Consult the [Local Setup Guide](./docs/local_setup.md) for detailed setup instructions.

## 📜 License

This project is licensed under the Apache License 2.0. See the [LICENSE](./LICENSE) file.

## 🤝 Contributing & Disclaimer

This is a personal project by [Heiko Hotz](https://github.com/heiko-hotz) to explore Gemini capabilities. Suggestions and feedback are welcome via Issues or Pull Requests.

**This project is developed independently and does not reflect the views or efforts of Google.**
