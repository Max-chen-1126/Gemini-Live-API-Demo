# Gemini-Live-API-Demo

Gemini TTS (Text-to-Speech) API 完整示範專案，展示 Google Gemini 2.5 模型的原生語音生成功能。此專案支援單人語音轉換和多人對話生成，適用於 Podcast 製作、有聲書創建和教學內容開發。

## 🚀 主要功能

- **單人語音生成**：30+ 種預設語音選項，支援不同風格（專業、成熟、清晰、資訊豐富等）
- **多人對話生成**：支援多角色語音對話，每個角色可使用不同聲音
- **多語言支援**：自動語言偵測，支援中文、英文等 24 種語言
- **高品質音訊**：24kHz 採樣率、16位元、單聲道 WAV 格式輸出
- **自然語言控制**：透過提示詞精確控制語音風格、語氣和表達方式

## 🛠️ 環境設定

### 系統需求
- Python 3.11 或更高版本
- Google API 金鑰 (需啟用 Gemini API)

### 安裝依賴
```bash
# 使用 uv 安裝依賴（推薦）
uv sync

# 或使用 pip
pip install google-genai python-dotenv ipykernel
```

### 環境變數設定
1. 建立 `.env` 檔案於專案根目錄
2. 加入你的 Google API 金鑰：
```bash
GOOGLE_API_KEY=your_api_key_here
```

## 📚 主要示範內容

### test_gemini_native_api.ipynb

這是專案的核心示範 notebook，包含以下完整功能展示：

#### 🎯 **支援的 TTS 模型**
- `gemini-2.5-flash-preview-tts`：快速 TTS 生成
- `gemini-2.5-pro-preview-tts`：高品質 TTS 生成

#### 🎵 **單人語音生成範例**
1. **專業客服語音** (Gacrux - 成熟風格)
   - 範例：「尊敬的客戶你好，目前電話都在忙線中，請稍等」
   - 輸出：`audio/Gacrux_01.wav`

2. **會議主持語音** (Erinome - 清晰風格)  
   - 範例：「歡迎來到這場會議，今天主要重點討論 Gemini 有哪些語音的功能」
   - 輸出：`audio/Erinome_01.wav`

3. **活潑解說語音** (Charon - 資訊豐富風格)
   - 範例：「通過 Gemini TTS 我們甚至可以生成與 NotebookLM Audio 一樣的 Podcast」
   - 輸出：`audio/charon_02.wav`

#### 👥 **多人對話生成範例**
- **教學對話**：特斯拉超級充電站操作指南
- **角色設定**：
  - 講師 (Puck 聲音)：語氣專業，指令清晰
  - 新車主 (Zephyr 聲音)：專注提問關鍵操作
- **輸出**：`audio/multi_01.wav`

#### 🔧 **核心功能函數**
- `generate_tts(PROMPT, VOICE, FILENAME)`：封裝的 TTS 生成函數
- `wave_file(filename, pcm, channels, rate, sample_width)`：音訊檔案保存工具

## 🎨 可用語音風格

| 語音名稱 | 風格特色 | 適用場景 |
|---------|---------|----------|
| Leda | 標準 | 一般用途 |
| Gacrux | 成熟 | 專業客服、正式場合 |
| Erinome | 清晰 | 會議主持、教學 |
| Charon | 資訊豐富 | 解說、介紹 |
| Puck | 樂觀 | 積極正面的內容 |
| Zephyr | 自然 | 對話、訪談 |

## 📁 專案結構

```
Gemini-Live-API-Demo/
├── README.md                              # 專案說明
├── main.py                               # 基本執行入口
├── pyproject.toml                        # 專案配置和依賴
├── uv.lock                              # 依賴鎖定檔案
├── notebook/
│   └── test_gemini_native_api.ipynb     # 主要示範 notebook
└── audio/                               # 生成的音訊檔案
    ├── single_voice_out.wav             # 單人語音範例
    ├── Gacrux_01.wav                    # 客服語音
    ├── Erinome_01.wav                   # 主持語音
    ├── charon_02.wav                    # 解說語音
    └── multi_01.wav                     # 多人對話
```

## 🚀 使用方式

### 啟動 Jupyter Notebook
```bash
# 啟動 Jupyter
jupyter notebook

# 或直接開啟示範 notebook
jupyter notebook notebook/test_gemini_native_api.ipynb
```

### 基本使用範例
```python
# 載入必要模組
from google import genai
from google.genai import types

# 生成單人語音
response = client.models.generate_content(
    model="gemini-2.5-flash-preview-tts",
    contents="你好，歡迎使用 Gemini TTS！",
    config=types.GenerateContentConfig(
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Leda"
                )
            )
        )
    )
)
```

## 🎯 應用場景

- **Podcast 製作**：多人對話內容生成
- **有聲書創建**：長篇文本轉語音
- **教學內容**：互動式教學對話
- **客服系統**：自動語音回應
- **內容創作**：多媒體內容配音

## 📝 注意事項

- 模型僅接受純文字輸入，輸出純音訊格式
- 上下文長度限制為 32k tokens
- 中文支援在早期測試階段，建議搭配英文指令使用
- API 呼叫需要有效的 Google API 金鑰和適當的配額

## 🔗 相關資源

- [Gemini TTS 官方文件](https://ai.google.dev/gemini-api/docs/speech-generation)
- [Google AI Studio](https://aistudio.google.com/)

---

**Link**: [Test Gemini native TTS](notebook/test_gemini_native_api.ipynb)