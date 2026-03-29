# Flask Backend Dev

一個使用 Flask 與 MongoDB Atlas 實作的基礎會員系統範例，包含：

- 會員註冊
- 會員登入
- 會員頁面（Session 驗證）
- 會員登出
- 錯誤訊息頁面

## 功能簡介

此專案提供最小可運作的會員流程：

1. 使用者可在註冊頁輸入信箱、帳號、密碼建立會員
2. 系統會檢查信箱是否重複
3. 使用者可登入並進入會員頁
4. 登入成功後以 Session 保存會員帳號資訊
5. 登出後移除 Session 並返回首頁

## 技術棧

- Python 3.10+
- Flask
- PyMongo
- python-dotenv
- MongoDB Atlas

## 專案結構

```text
Flask-Backend-Dev/
├─ app.py
├─ .env.example
├─ public/
└─ templates/
   ├─ index.html
   ├─ register.html
   ├─ member.html
   ├─ success.html
   └─ error.html
```

## 安裝與執行

### 1) 建立虛擬環境（建議）

Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) 安裝依賴套件

```powershell
pip install flask pymongo python-dotenv
```

### 3) 設定環境變數

先建立 `.env`：

```powershell
Copy-Item .env.example .env
```

接著編輯 `.env`，填入你的 MongoDB 連線資訊與 Secret Key。

範例：

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/?appName=<app-name>
SECRET_KEY=replace-with-a-long-random-secret
```

本專案在 `app.py` 使用 `load_dotenv()`，啟動時會自動讀取 `.env`。
此外，`app.py` 已使用 `if __name__ == "__main__":` 包住 `app.run(...)`，避免被 import 時直接啟動伺服器。

### 4) 啟動專案

```powershell
python app.py
```

伺服器會啟動於：

- http://127.0.0.1:3000

若未設定 `MONGODB_URI` 或 `SECRET_KEY`，程式會在啟動時拋出錯誤。

`.env` 已加入 `.gitignore`，環境變數不會被 Git 追蹤。

## 路由說明

| Method | Path | 說明 |
|---|---|---|
| GET | / | 首頁（登入表單） |
| GET | /register | 註冊頁 |
| POST | /signup | 建立會員 |
| POST | /signin | 會員登入 |
| GET | /member | 會員頁（需登入） |
| GET | /signout | 登出 |
| GET | /error?msg=... | 錯誤頁 |

## 資料庫說明

- Database: `member_system`
- Collection: `users`
- 文件欄位：
  - `email` (string)
  - `account` (string)
  - `password` (string)

## 使用流程

1. 開啟首頁並點選「註冊會員」
2. 完成註冊後返回首頁
3. 使用註冊的信箱與密碼登入
4. 成功後進入會員頁，可執行登出

## 注意事項（重要）

目前程式已改為透過 `.env` 讀取敏感資訊（`MONGODB_URI`、`SECRET_KEY`）。

建議後續改進：

- 密碼應加鹽雜湊後儲存（例如 `werkzeug.security` 或 `bcrypt`）
- 補上輸入驗證與錯誤處理機制

## 授權

此專案目前未附授權條款，如需公開使用，建議新增 `LICENSE` 檔案（例如 MIT）。
