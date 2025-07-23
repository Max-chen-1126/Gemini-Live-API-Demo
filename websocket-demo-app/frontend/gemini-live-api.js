class GeminiLiveResponseMessage {
    constructor(data) {
        this.data = "";
        this.type = "";
        this.endOfTurn = data?.serverContent?.turnComplete;

        const parts = data?.serverContent?.modelTurn?.parts;

        if (data?.setupComplete) {
            this.type = "SETUP COMPLETE";
        } else if (parts?.length && parts[0].text) {
            this.data = parts[0].text;
            this.type = "TEXT";
        } else if (parts?.length && parts[0].inlineData) {
            this.data = parts[0].inlineData.data;
            this.type = "AUDIO";
        }
    }
}

class GeminiLiveAPI {
    constructor(proxyUrl, model) {
        this.proxyUrl = proxyUrl;
        this.model = model;
        this.modelUri = `models/${this.model}`;

        this.responseModalities = ["AUDIO"];
        this.systemInstructions = "";
        this.languageCode = "cmn-CN";

        this.onReceiveResponse = (message) => {
            console.log("Default message received callback", message);
        };

        this.onConnectionStarted = () => {
            console.log("Default onConnectionStarted");
        };

        this.onErrorMessage = (message) => {
            alert(message);
        };

        this.apiKey = "";
        this.websocket = null;

        console.log("Created Gemini Live API object: ", this);
    }

    setApiKey(newApiKey) {
        console.log("setting API key: ", newApiKey);
        this.apiKey = newApiKey;
    }

    connect(apiKey) {
        this.setApiKey(apiKey);
        this.setupWebSocketToService();
    }

    disconnect() {
        this.webSocket.close();
    }

    sendMessage(message) {
        this.webSocket.send(JSON.stringify(message));
    }

    onReceiveMessage(messageEvent) {
        console.log("Message received: ", messageEvent);
        const messageData = JSON.parse(messageEvent.data);
        const message = new GeminiLiveResponseMessage(messageData);
        console.log("onReceiveMessageCallBack this ", this);
        this.onReceiveResponse(message);
    }

    setupWebSocketToService() {
        console.log("connecting: ", this.proxyUrl);

        this.webSocket = new WebSocket(this.proxyUrl);

        this.webSocket.onclose = (event) => {
            console.log("websocket closed: ", event);
            this.onErrorMessage("Connection closed");
        };

        this.webSocket.onerror = (event) => {
            console.log("websocket error: ", event);
            this.onErrorMessage("Connection error");
        };

        this.webSocket.onopen = (event) => {
            console.log("websocket open: ", event);
            this.sendInitialSetupMessages();
            this.onConnectionStarted();
        };

        this.webSocket.onmessage = this.onReceiveMessage.bind(this);
    }

    sendInitialSetupMessages() {
        // Send API key to the proxy server
        const serviceSetupMessage = {
            api_key: this.apiKey,
        };
        this.sendMessage(serviceSetupMessage);

        // Setup session configuration for Google AI Studio
        // NOTE: Google APIs use snake_case for JSON keys.
        const generationConfig = {
            response_modalities: this.responseModalities,
        };

        if (this.languageCode) {
            generationConfig.speech_config = {
                language_code: this.languageCode,
                voice_config: {
                    prebuilt_voice_config: {
                        voice_name: "Charon"
                    }
                }
            };
        }

        // Explicitly configure VAD and barge-in (interrupt) behavior.
        // NOTE: These are the default settings, but it's good practice to be explicit.
        const realtimeInputConfig = {
            // Use the server's automatic voice activity detection with high sensitivity.
            automatic_activity_detection: {
                // How likely speech is to be detected.
                start_of_speech_sensitivity: "START_SENSITIVITY_HIGH",
                // Required duration of speech before committing. Lower is more sensitive.
                prefix_padding_ms: 100,
                // How likely speech is to be ended.
                end_of_speech_sensitivity: "END_SENSITIVITY_HIGH",
            },
            // Interrupt the model's response when the user starts speaking.
            activity_handling: "START_OF_ACTIVITY_INTERRUPTS",
        };

        const sessionSetupMessage = {
            setup: {
                model: this.modelUri,
                generation_config: generationConfig,
                system_instruction: { parts: [{ text: this.systemInstructions }] },
                realtime_input_config: realtimeInputConfig,
            },
        };
        this.sendMessage(sessionSetupMessage);
    }

    sendTextMessage(text) {
        const textMessage = {
            client_content: {
                turns: [
                    {
                        role: "user",
                        parts: [{ text: text }],
                    },
                ],
                turn_complete: true,
            },
        };
        this.sendMessage(textMessage);
    }

    sendRealtimeInputMessage(data, mime_type) {
        // NOTE: `media_chunks` is deprecated. Use `audio` or `video` fields instead.
        const message = {
            realtime_input: {},
        };

        const blob = {
            mime_type: mime_type,
            data: data,
        };

        if (mime_type.startsWith("audio/")) {
            message.realtime_input.audio = blob;
        } else if (mime_type.startsWith("image/")) {
            message.realtime_input.video = blob;
        }
        this.sendMessage(message);
    }

    sendAudioMessage(base64PCM) {
        this.sendRealtimeInputMessage(base64PCM, "audio/pcm");
    }

    sendImageMessage(base64Image, mime_type = "image/jpeg") {
        this.sendRealtimeInputMessage(base64Image, mime_type);
    }
}

console.log("loaded gemini-live-api.js");
