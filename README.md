# Gemini Live API Demo

**探索 Gemini AI 的語音和多模態能力！本專案整合了多個 Google Gemini API 演示，包括文字轉語音 (TTS) 功能和即時多模態對話應用。**

本專案包含四個主要演示模組：
- **Gemini TTS 原生 API** - 單人/多人語音生成
- **Live API 多模態互動** - 即時雙向語音視訊對話  
- **即時聊天 Web 應用** - 完整的多模態聊天介面
- **WebSocket 演示應用** - 基於 Google AI Studio 的簡化版本

## 🚀 快速開始

### 前置需求
- Python 3.11+
- Google Gemini API 金鑰 ([申請連結](https://makersuite.google.com/app/apikey))
- uv 套件管理器 (推薦) 或 pip

### 基本安裝
```bash
# 複製專案
git clone <your-repo-url>
cd Gemini-Live-API-Demo

# 安裝依賴
uv sync  # 或 pip install google-genai python-dotenv ipykernel

# 設定環境變數
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

各演示模組有獨立的使用說明，請參考各資料夾內的 README.md 文件。

## 📁 專案結構

```
Gemini-Live-API-Demo/
├── README.md                                    # 專案總覽 (本檔案)
├── main.py                                     # 基本 API 測試入口
├── pyproject.toml                              # Python 專案配置
├── LICENSE                                     # Apache 2.0 授權條款
├── NOTICE                                      # 歸屬聲明
├── CLAUDE.md                                   # AI 助手指引
│
├── 📂 test_gemini_native_api/                  # 🎵 TTS 原生 API 演示
│   ├── test_gemini_native_api.ipynb           # Jupyter 互動演示
│   └── README.md                              # → TTS 詳細使用說明
│
├── 📂 intro_multimodal_live_api_genai_sdk/    # 🎤 Live API 多模態演示  
│   ├── intro_multimodal_live_api_genai_sdk.ipynb  # Live API 完整功能
│   └── README.md                              # → Live API 詳細說明
│
├── 📂 project-liveapidemo/                    # 🖥️ 即時聊天 Web 應用
│   ├── client/                                # 前端應用 (HTML/JS)
│   ├── server/                                # 後端伺服器 (Python)
│   ├── docs/                                  # 設定文件
│   └── README.md                              # → Web 應用使用說明
│
├── 📂 websocket-demo-app/                     # 🔗 WebSocket 簡化演示
│   ├── frontend/                              # 前端 HTML 應用
│   ├── backend/                               # Python WebSocket 伺服器
│   └── README.md                              # → WebSocket Demo 說明
│
└── 📂 audio/                                   # 🔊 生成的音訊檔案
    ├── *.wav                                  # TTS 生成的語音檔案
    └── README.md                              # → 音訊檔案說明
```

## 📖 演示模組說明

### 🎵 [test_gemini_native_api/](test_gemini_native_api/)
**Gemini TTS 原生 API 演示**
- 單人語音生成 (30+ 種語音風格) 
- 多人對話生成 (角色專屬語音)
- 互動式 Jupyter Notebook 教學
- 詳細說明: [→ TTS README](test_gemini_native_api/README.md)

### 🎤 [intro_multimodal_live_api_genai_sdk/](intro_multimodal_live_api_genai_sdk/)
**Live API 多模態互動演示**
- 即時雙向語音和視訊互動
- 文字轉音訊對話、Google 搜尋、語音轉錄
- 語音活動檢測 (VAD)、情感對話
- 詳細說明: [→ Live API README](intro_multimodal_live_api_genai_sdk/README.md)

### 🖥️ [project-liveapidemo/](project-liveapidemo/)
**即時聊天 Web 應用**
- 完整的多模態聊天介面 (桌面版/行動版)
- 即時語音對話、螢幕分享、網路攝影機
- 語音中斷、即時轉錄功能
- 詳細說明: [→ Web 應用 README](project-liveapidemo/README.md)

### 🔗 [websocket-demo-app/](websocket-demo-app/)
**WebSocket 簡化演示**
- 基於 Google AI Studio 的輕量版本
- 僅需 API Key，無需複雜設定
- 適合快速上手和原型開發
- 詳細說明: [→ WebSocket Demo README](websocket-demo-app/README.md)

### 🔊 [audio/](audio/)
**生成的音訊檔案**
- TTS 演示生成的 WAV 音訊檔案
- 包含單人語音和多人對話範例
- 詳細說明: [→ 音訊檔案 README](audio/README.md)

## 📄 授權與歸屬

本專案基於 [Apache License 2.0](LICENSE) 授權。詳細歸屬資訊請參考 [NOTICE](NOTICE) 檔案。

### 原始專案歸屬
- **project-liveapidemo** 基於 [Heiko Hotz](https://github.com/heiko-hotz) 的 [Project Livewire](https://github.com/heiko-hotz/project-livewire) 開發
- **其他模組** 基於 Google GenAI SDK 範例和官方文件開發

### 使用聲明
**⚠️ 本專案僅供教學和演示用途，不得用於商業目的。**

## 🤝 貢獻與支援

歡迎透過 GitHub Issues 提出問題或建議。請遵循現有程式碼風格並更新相關文件。

---

**免責聲明**：本專案獨立開發，不代表 Google 或其他組織的觀點或立場。