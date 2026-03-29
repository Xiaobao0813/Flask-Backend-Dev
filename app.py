# 初始化資料庫連線
import os
from pymongo import * # 載入 pymongo 模組套件
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
# 連線到 MongoDB 雲端資料庫
load_dotenv()
db_uri = os.getenv("MONGODB_URI")
if not db_uri:
    raise RuntimeError("環境變數 MONGODB_URI 尚未設定")
# 創建一個新帳戶然後連線到伺服器
client = MongoClient(db_uri, server_api=ServerApi('1'))
# 傳送 ping 訊號去確認是否成功連線
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
# 建立 member_system 資料庫
db = client.member_system
print("資料庫連線建立成功")

# 載入 Flask 所有相關工具
from flask import *
# 建立 Application 物件，並設置靜態檔案處理
app = Flask(__name__, static_folder="public", static_url_path="/")
# 設定 Session 密鑰
app.secret_key = os.getenv("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("環境變數 SECRET_KEY 尚未設定")
# 處理路由
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/member")
def member():
    if "account" in session:
        data = session["account"]
        return render_template("member.html", account=data)
    else:
        return redirect("/")

@app.route("/error") # /error?msg=錯誤訊息
def error():
    msg = request.args.get("msg", "發生錯誤，請聯繫客服。")
    return render_template("error.html", message = msg)

@app.route("/signup", methods=["POST"])
def signup():
    # 從前端接收資料
    email = request.form["email"].strip()
    account = request.form["account"].strip()
    password = request.form["password"].strip()
    # 檢查三筆資料都有輸入
    if not all([email, account, password]):
        return redirect("/error?msg=請完整輸入三筆資料")
    else:
        # 根據資料，和資料庫互動
        collection=db.users
        # 檢查會員集合中是否有相同的 email 資料
        result = collection.find_one({
            "email":email
        })
        if result != None:
            return redirect("/error?msg=信箱已被註冊")
        # 把資料放進資料庫中，完成註冊
        else:
            collection.insert_one({
                "email":email,
                "account":account,
                "password":password
            })
            return render_template("success.html")

@app.route("/signin", methods=["POST"])
def signin():
    # 從前端取得使用者輸入資料
    email = request.form["email"].strip()
    password = request.form["password"].strip()
    # 檢查兩筆資料都有輸入
    if not all([email, password]):
        return redirect("/error?msg=請完整輸入兩筆資料")
    else:
        # 和資料庫互動
        collection=db.users
        # 檢查信箱密碼是否正確
        result=collection.find_one({
            "$and":[
                {"email":email},
                {"password":password}
            ]
        })
        # 找不到對應的資料，登入失敗，導向到錯誤頁面
        if result == None:
            return redirect("/error?msg=信箱或密碼輸入錯誤")
        # 登入成功，在 session 紀錄會員資訊，導向到會員頁面
        else:
            session["account"] = result["account"]
            return redirect("/member")

@app.route("/signout")
def signout():
    # 移除 session 中的會員資訊
    del session["account"]
    return redirect("/")

# 啟動伺服器在 Port 3000
if __name__ == "__main__":
    app.run(port=3000)