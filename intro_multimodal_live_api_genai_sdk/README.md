# Gemini Live API 多模態互動示範

本專案展示了 Google Gemini Live API 的多種功能，包括低延遲的雙向語音和視頻互動功能。透過 Google Gen AI SDK，您可以體驗文字、音訊和視頻的輸入處理，以及文字和音訊輸出生成。

## 專案概述

Gemini Live API 是 Google 推出的即時互動 API，支援：
- **低延遲雙向通訊**：實現自然的對話體驗
- **多模態輸入**：支援文字、音訊、視頻輸入
- **多樣化輸出**：提供文字和音訊回應
- **進階功能**：包含語音活動檢測、情感對話、主動式音訊等

## 環境設置

### 系統需求
- Python 3.11+
- Google API Key（需要存取 Gemini Live API 的權限）

### 依賴套件安裝

```bash
# 使用 uv 安裝依賴（推薦）
uv sync

# 或使用 pip 安裝主要套件
pip install google-genai python-dotenv numpy ipython jupyter
```

### 環境變數配置

1. 在專案根目錄建立 `.env` 檔案：
```bash
GOOGLE_API_KEY=你的_Google_API_Key
```

2. 在 Google AI Studio 或 Google Cloud Console 中取得 API Key
3. 確保 API Key 有存取 Gemini Live API 的權限

### 執行 Notebook

```bash
# 啟動 Jupyter Notebook
jupyter notebook

# 開啟 intro_multimodal_live_api_genai_sdk.ipynb
```

## 支援的模型

### 1. gemini-live-2.5-flash-preview
- **特色**：通用型 Live API 模型
- **功能**：文字對話、音訊生成、工具呼叫、語音轉錄
- **適用場景**：一般互動應用、客服機器人、語音助理

### 2. gemini-2.5-flash-preview-native-audio-dialog
- **特色**：原生音訊對話模型（需使用 v1alpha API）
- **功能**：增強的語音品質、主動式音訊、情感對話
- **適用場景**：高品質語音互動、情感感知應用

## 功能範例

### Gemini 2.0 Flash 範例

#### 1. 文字對文字生成
基本的文字對話功能，模型接收文字輸入並回傳文字回應。

```python
async with client.aio.live.connect(
    model="gemini-live-2.5-flash-preview",
    config=LiveConnectConfig(response_modalities=[Modality.TEXT]),
) as session:
    await session.send_client_content(
        turns=Content(role="user", parts=[Part(text="你好，Gemini！")])
    )
```

#### 2. 文字轉音訊生成
將文字轉換為語音輸出，支援多種預建語音選項。

**支援的語音選項**：
- Aoede, Puck, Charon, Kore, Fenrir
- Leda, Orus, Zephyr

**語言支援**：
- `cmn-CN`：簡體中文
- `en-US`：美式英語
- 其他語言請參考官方文件

```python
config = LiveConnectConfig(
    response_modalities=["AUDIO"],
    speech_config=SpeechConfig(
        voice_config=VoiceConfig(
            prebuilt_voice_config=PrebuiltVoiceConfig(voice_name="Zephyr")
        ),
        language_code="cmn-CN",
    ),
)
```

#### 3. 文字轉音訊對話
建立持續的對話 session，使用者可以連續輸入文字並接收音訊回應。

#### 4. Google 搜尋功能
整合 Google 搜尋工具，讓模型可以查詢即時資訊。

```python
config = LiveConnectConfig(
    response_modalities=["TEXT"],
    tools=[Tool(google_search=GoogleSearch())],
)
```

#### 5. 音訊轉錄
將輸入和輸出的音訊轉換為文字，便於記錄和分析。

```python
config = LiveConnectConfig(
    input_audio_transcription=AudioTranscriptionConfig(),
    output_audio_transcription=AudioTranscriptionConfig(),
)
```

#### 6. 語音活動檢測 (VAD)
自動檢測使用者的語音活動，支援自然的對話中斷和恢復。

```python
config = LiveConnectConfig(
    realtime_input_config=RealtimeInputConfig(
        automatic_activity_detection=AutomaticActivityDetection(
            start_of_speech_sensitivity=StartSensitivity.START_SENSITIVITY_LOW,
            end_of_speech_sensitivity=EndSensitivity.END_SENSITIVITY_LOW,
        )
    ),
)
```

### Gemini 2.5 Flash Native Audio 範例

#### 1. 主動式音訊 (Proactive Audio)
模型只在相關時才回應，智能判斷查詢是否針對裝置，避免不必要的回應。

```python
config = LiveConnectConfig(
    response_modalities=["AUDIO"],
    proactivity=ProactivityConfig(proactive_audio=True),
)
```

#### 2. 情感對話 (Affective Dialog)
理解並適當回應使用者的情感表達，提供更細緻的對話體驗。

```python
config = LiveConnectConfig(
    response_modalities=["AUDIO"],
    enable_affective_dialog=True,
)
```

## 音訊規格

- **取樣率**：24kHz
- **位元深度**：16-bit
- **聲道**：單聲道 (Mono)
- **格式**：PCM

## 使用指南

### 1. 基本使用流程

1. **建立連線**：使用 `client.aio.live.connect()` 建立 WebSocket 連線
2. **配置參數**：設定回應模式、語音配置、工具等
3. **發送訊息**：使用 `session.send_client_content()` 發送使用者輸入
4. **接收回應**：透過 `session.receive()` 取得模型回應
5. **處理音訊**：將音訊資料轉換為可播放格式

### 2. Session 管理

- 每個 session 代表一個 WebSocket 連線
- Session 保存對話歷史，但結束後會清除
- 使用 `async with` 確保連線正確關閉

### 3. 最佳實踐

#### 音訊處理
```python
# 正確的音訊資料處理方式
audio_data = []
async for message in session.receive():
    if message.server_content.model_turn:
        for part in message.server_content.model_turn.parts:
            if part.inline_data:
                audio_data.append(
                    np.frombuffer(part.inline_data.data, dtype=np.int16)
                )

# 播放音訊
if audio_data:
    display(Audio(np.concatenate(audio_data), rate=24000, autoplay=True))
```

#### 錯誤處理
- 監聽 `message.server_content.interrupted` 處理中斷
- 適當設定 VAD 參數避免誤觸發
- 處理網路連線異常

#### 效能優化
- 合理設定 `prefix_padding_ms` 和 `silence_duration_ms`
- 避免過於頻繁的 API 呼叫
- 使用適合的語音靈敏度設定

## 常見問題

### Q: 如何選擇適合的語音？
A: 根據應用場景選擇：
- **Zephyr**：通用、自然的語音
- **Puck**：活潑、年輕的語音
- **Charon**：專業、成熟的語音

### Q: 為什麼音訊品質不佳？
A: 檢查以下設定：
- 確保設定正確的 `language_code`
- 使用適合的語音選項
- 檢查網路連線品質

### Q: 如何處理對話中斷？
A: 使用 VAD 功能：
- 調整 `start_of_speech_sensitivity` 和 `end_of_speech_sensitivity`
- 監聽 `interrupted` 事件
- 適當處理音訊串流結束

## 參考資源

- [Gemini Live API 官方文件](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/multimodal-live)
- [Google Gen AI SDK](https://github.com/google/generative-ai-python)
- [語音選項參考](https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/multimodal-live#voices)

## 授權

本專案僅供學習和測試使用。使用 Gemini Live API 需遵守 Google 的服務條款和使用政策。