# 📱 清大徵才攤位定位系統 - 手機使用指南

## 🚀 運行方式

### 方法 1️⃣：本地運行（電腦 → 手機）
1. 安裝依賴：
```bash
pip install -r requirements.txt
```

2. 啟動應用：
```bash
streamlit run streamlit_app.py
```

3. 在電腦上開啟網址（通常是 `http://localhost:8501`）

4. **在手機上訪問**：
   - 確保手機和電腦連接到同一個 WiFi
   - 在電腦命令提示字元中尋找這樣的信息：
     ```
     You can now view your Streamlit app in your browser.

     Local URL: http://localhost:8501
     Network URL: http://192.168.x.x:8501  ← 使用這個網址
     ```
   - 在手機瀏覽器輸入 `http://192.168.x.x:8501`

---

### 方法 2️⃣：雲端部署（完全免費）

#### 使用 Streamlit Cloud（推薦！）
1. 上傳到 GitHub：
   - 新建 GitHub Repo
   - 上傳 `streamlit_app.py` 和 `requirements.txt`

2. 訪問 https://share.streamlit.io/
   - 登錄 GitHub 帳號
   - 選擇你的 Repo
   - Streamlit 會自動部署

3. 完成！你會獲得一個永久網址，可以在任何地方訪問（包括手機）

---

#### 使用 Heroku / Railway（其他選擇）
- 也可以部署到 Heroku（免費額度已停止）或 Railway
- 詳細步驟可詢問

---

## 📱 在手機上用書籤快速訪問

### iOS（iPhone/iPad）
1. 在 Safari 中打開應用網址
2. 點擊底部分享按鈕 → 「新增至主畫面」
3. 命名為「徵才攤位」
4. 完成！現在像 App 一樣可以直接點擊

#### iOS 若出現骨架畫面卡住（重要）
- 這通常是 iOS「主畫面獨立模式」對 Streamlit WebSocket 的相容性限制，不是程式功能錯誤。
- 請改用以下方式，穩定度最高：
   1. 打開 iOS「捷徑」App → 新增捷徑。
   2. 動作選「打開 URL」，填入你的 Streamlit 網址。
   3. 將此捷徑「加入主畫面」。
   4. 之後從主畫面點圖示，會直接用 Safari 開啟（不是獨立模式），通常可避免卡骨架。

### Android
1. 在 Chrome 中打開網址
2. 點擊右上角三點 → 「安裝應用」或「新增至主畫面」
3. 完成！

---

## 🎯 功能特點

✅ **即時資料**：自動從清大徵才網站爬取最新企業資訊  
✅ **模糊搜尋**：支援企業名稱模糊查詢  
✅ **地圖定位**：自動判斷攤位所在區域  
✅ **離線可用**：資料加載後支援離線查詢  
✅ **響應式設計**：完全適配手機螢幕  
✅ **數據匯出**：可下載 CSV 格式的企業列表  

---

## 🆘 常見問題

**Q：為什麼在手機上打不開？**  
A：確認手機和電腦在同一個 WiFi，並檢查防火牆設定

**Q：怎樣讓應用一直在線？**  
A：部署到 Streamlit Cloud（推薦），99% 免費

**Q：可以下載成離線 App 嗎？**  
A：可以用 PWA 技術實現，詢問我可提供另一個版本

---

## 💡 建議

- **最簡單**：用本地方法 + 手機 WiFi 訪問（現在就能用）
- **最穩定**：部署到 Streamlit Cloud（任何地方都能用）
- **最像 App**：用「新增至主畫面」功能（看起來像真正的 App）

需要幫忙嗎？😊

---

## 🍎 iOS 主畫面穩定方案（推薦）

若 iOS 透過主畫面開啟 Streamlit 持續卡在骨架畫面，建議改用本專案提供的「靜態版」：

- 靜態版入口：[docs/index.html](docs/index.html)
- 資料檔：[docs/booth_data.json](docs/booth_data.json)

### 為什麼這個版本穩定
- 不使用 Streamlit WebSocket
- 不依賴伺服器 Session
- 內容為固定資料，適合 iOS 主畫面啟動

### 如何啟用（GitHub Pages）
1. 到 GitHub Repo 的 Settings -> Pages
2. Source 選擇 `Deploy from a branch`
3. Branch 選 `main`，資料夾選 `/docs`
4. 儲存後等待部署完成
5. 用 iPhone 開啟 Pages 網址後「加入主畫面」

> 這個做法通常比 Streamlit 在 iOS 主畫面模式更可靠。
