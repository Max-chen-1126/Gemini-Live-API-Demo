# Gemini Live API Demo (Google AI Studio)

在這個教程中，您將構建一個網頁應用程式，讓您能夠使用語音和攝像頭與 Gemini 2.5 通過 Google AI Studio Live API 進行對話。

Google AI Studio Live API 是一個低延遲雙向串流 API，支援音頻和視頻串流輸入，並能輸出音頻。此版本已修改為使用 Google AI Studio 的 Live API，只需要 API Key 即可開始使用，比原本的 Vertex AI 版本更簡單。

## 架構

- **後端 (Python WebSockets 伺服器):** 處理認證並作為前端和 Gemini API 之間的中介
- **前端 (HTML/JavaScript):** 提供用戶介面並通過 WebSockets 與後端互動

## 前置需求

- Google AI Studio API Key (在 https://aistudio.google.com/app/apikey 獲取)
- Python 3.11 或更高版本
- 支援 WebSocket 的現代網頁瀏覽器
- 雖然有一些網頁開發經驗會有幫助，但本教程提供了逐步指導

## 檔案結構

- `backend/main.py`: Python 後端代碼
- `backend/requirements.txt`: 列出所需的 Python 依賴項

- `frontend/index.html`: 前端 HTML 應用程式
- `frontend/script.js`: 主要前端 JavaScript 代碼
- `frontend/gemini-live-api.js`: 與 Gemini API 互動的腳本
- `frontend/live-media-manager.js`: 處理媒體輸入和輸出的腳本
- `frontend/pcm-processor.js`: 處理 PCM 音頻的腳本
- `frontend/cookieJar.js`: 管理 cookies 的腳本

## 設置說明

### 本地設置

1. 克隆儲存庫並進入正確的目錄

    ```sh
    git clone <your-repository-url>
    cd websocket-demo-app
    ```

2. 創建新的虛擬環境並激活它：

    ```sh
    python3 -m venv env
    source env/bin/activate  # 在 Windows 上使用：env\Scripts\activate
    ```

3. 安裝依賴項：

    ```sh
    pip3 install -r backend/requirements.txt
    ```

4. 啟動 Python WebSocket 伺服器：

    ```sh
    python3 backend/main.py
    ```

    您應該看到：
    ```
    Running websocket server localhost:8080...
    ```

5. 啟動前端：

    在**另一個**終端視窗中（保持後端伺服器運行）：

    ```sh
    cd frontend
    python3 -m http.server 8000
    ```

6. 在瀏覽器中打開演示應用程式：

    導航到 `http://localhost:8000`

7. 獲取您的 Google AI Studio API Key：

    - 訪問 https://aistudio.google.com/app/apikey
    - 創建新的 API Key
    - 複製 API Key

8. 連接並與演示互動：

    - 將您的 API Key 輸入到「API Key」欄位中
    - 可選：修改系統指令和語言代碼設置
    - 按下「Connect」按鈕連接您的網頁應用程式
    - 現在您可以與 Gemini 2.5 通過 Google AI Studio Live API 互動了

## 如何與應用程式互動

- **文字輸入**: 您可以在文字框中輸入文字提示並按下發送箭頭。模型將通過音頻回應（記得調高音量！）
- **語音輸入**: 按下麥克風按鈕開始說話。模型將通過音頻回應。如果您想關閉麥克風，請按下帶有斜線的麥克風按鈕
- **視頻輸入**: 模型也會捕獲您的攝像頭輸入並發送給 Gemini。您可以詢問關於當前或之前視頻片段的問題

## 特色功能

### 多模態支援
- **音頻輸入**: 即時語音識別和處理
- **視頻輸入**: 攝像頭和螢幕分享支援
- **文字輸入**: 傳統文字聊天介面

### 音頻輸出
- 使用 Gemini 的原生 TTS（文字轉語音）功能
- 支援多種預設語音（預設使用 "Charon" 語音）
- 高品質 24kHz 音頻輸出

### 即時互動
- 低延遲雙向通信
- 自動語音活動檢測
- 支援中斷模式（當用戶開始說話時中斷模型回應）

### 配置選項
- **系統指令**: 自定義模型行為
- **語言代碼**: 支援多語言（預設：中文 cmn-CN）
- **回應模式**: 選擇音頻或文字回應
- **設備選擇**: 動態選擇攝像頭和麥克風

## 技術細節

### 使用的模型
- `gemini-live-2.5-flash-preview`: 快速且高效的即時互動模型

### 認證方式
- 使用 Google AI Studio API Key（比 Vertex AI 的 Bearer Token 更簡單）
- API Key 通過 WebSocket 查詢參數傳遞給 Google AI Studio

### 網絡架構
- 前端通過 WebSocket 連接到本地代理伺服器 (localhost:8080)
- 代理伺服器轉發請求到 Google AI Studio Live API 端點
- 端點：`wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent`

## 故障排除

### 常見問題

1. **連接失敗**
   - 確保後端伺服器正在運行 (localhost:8080)
   - 檢查 API Key 是否正確
   - 確認網絡連接正常

2. **音頻問題**
   - 檢查瀏覽器是否有麥克風權限
   - 確保音量已調高
   - 嘗試重新選擇音頻設備

3. **視頻問題**
   - 檢查瀏覽器是否有攝像頭權限
   - 確認選擇了正確的攝像頭設備

### 開發者注意事項

- 所有用戶配置會自動保存到 cookies 中
- API Key 在前端以密碼形式儲存（生產環境請考慮更安全的方案）
- 支援響應式設計，適用於桌面和移動設備

## 安全性考量

- API Key 在前端明文儲存，僅適用於演示用途
- 生產環境建議在後端管理 API Key
- 所有通信都通過 HTTPS/WSS 加密

## 許可證和貢獻

此專案基於 Google AI Studio Live API 演示，旨在展示多模態 AI 互動的實現方式。