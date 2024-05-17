from fastapi import FastAPI, Request, Form, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import mysql.connector

app = FastAPI() # 產生 FastAPI 物件: FastAPI 框架下最核心物件
# 利用 uvicorn 去啟動伺服器在 http://127.0.0.1:8000  #uvicorn main:app --reload
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="secret_key") 

# 連線到資料庫
# 利用 mysql.connector 套件，呼叫 connect 方法，並提供帳號相關資訊
con = mysql.connector.connect(
    user = "root",
    password = "a32128466",
    host = "localhost",
    database = "website"
)
print("資料庫連線成功")

@app.get("/") # get會把要傳送的值放在header上，直接顯示在URL，不適合傳輸隱密資料
async def homepage(request: Request):
    return templates.TemplateResponse(
        "home.html", {"request": request, "title": "歡迎光臨，請註冊登入系統"})

@app.post("/signup") 
async def signup(
    # 從前端接收資料
    name: str = Form(), # = home.html 的 name 名，才能以相應的 name 提取表單資訊
    username: str = Form(),
    password: str = Form()): 
    # 根據接收到的資料，和資料庫互動
    con.reconnect() # 確認資料庫有順利連結，若無則重新連結
    cursor = con.cursor()
    cursor.execute("SELECT * FROM member WHERE username = %s", (username,))
    data = cursor.fetchone()
    if data: # 若有資料
        return RedirectResponse(url="/error?message=帳號已經被註冊", status_code=302)
    else:
        cursor.execute("INSERT INTO member(name, username, password) VALUES(%s, %s, %s)", (name, username, password))
        con.commit()
        return RedirectResponse(url="/", status_code=302)
    

@app.post("/signin") 
async def signin(request: Request,
    signedUsername: str = Form(),  
    signedPassword: str = Form()): 
    con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT id, name, username FROM member WHERE username = %s and password = %s", (signedUsername, signedPassword)) # Tuple
    data2 = cursor.fetchone()
    # print(data2) --> 為 Tuple
    if data2:
        id, name, username = data2  # Tuple Unpacking: 將 Turple 中多個資料指派給多個變數，等號左邊變數量 需= 等號右邊Tuple中元素量
        request.session["SIGNED-IN"] = True # 在 request.session 字典中設定名為 "SIGNED-IN" 的 key，其 Value = True
        request.session["ID"] = id # Record member id, username, name into the user state
        request.session["NAME"] = name
        request.session["USERNAME"] = username
        return RedirectResponse(url="/member", status_code=302) # code 默認為 307，重定向時保留原 HTTP 方法和數據 (post仍為post)，而 302 post 則可變 get
    else:
        return RedirectResponse(url="/error?message=帳號或密碼輸入錯誤", status_code=302)
  
@app.get("/member") 
async def member(request: Request):
    # 從 request 中獲取名為 "SIGNED-IN" 的 key，若 key 存在則返回其值，不存在則返回 False
    # if not = 若 "SIGNED-IN" 不存在 or 值 = False >> 表示未登入
    if not request.session.get("SIGNED-IN", False): 
        return RedirectResponse(url="/", status_code=302)
    
    name = request.session.get("NAME")
    id = request.session.get("ID")
    con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM message INNER JOIN member ON message.member_id = member.id ORDER BY message.time DESC")
    data3 = cursor.fetchall()
    return templates.TemplateResponse(
        "success.html", {"request": request, 
                         "title": "歡迎光臨，這是會員頁", 
                         "message": f"{name}，歡迎登入系統", # f-string 格式化字串: 字串前加f，可於字串中使用{}插入變數or表達式
                         "redirect":"登出系統",
                         "content": data3,
                         "id": id})
        
@app.get("/error") 
async def error(request: Request, message: str):
    return templates.TemplateResponse(
        "error.html", {"request": request, 
                       "title": "失敗頁面", 
                       "message": message, 
                       "redirect": "返回首頁"})

@app.get("/signout") 
async def signout(request: Request):
    request.session.clear() # 清除 session
    return RedirectResponse(url="/", status_code=302)

@app.post("/createMessage") 
async def content(request: Request,
    content: str = Form()):
    member_id = request.session.get("ID")
    con.reconnect()
    cursor = con.cursor()
    cursor.execute("INSERT INTO message(member_id, content) VALUES(%s, %s)", (member_id, content)) 
    con.commit()
    return RedirectResponse(url="/member", status_code=302)

@app.post("/deleteMessage") 
async def delete(request: Request,
    message_id: int = Form()):
    con.reconnect()
    cursor = con.cursor()
    cursor.execute("SELECT member.id FROM message INNER JOIN member ON message.member_id = member.id WHERE message.id = %s", (message_id, ))
    id = cursor.fetchone()
    member_id = request.session.get("ID")
    if id[0] == member_id:
        cursor.execute("DELETE FROM message WHERE id = %s", (message_id, )) # Tuple 只有一個值也要逗號
        con.commit()
        return RedirectResponse(url="/member", status_code=302)
    else:
        return RedirectResponse(url="/member", status_code=302)


@app.get("/api/member") 
# 用 Query 解析 URL 並獲取值: 以 username 為參數，若 URL 內沒有 username 參數/值則回傳 None
async def query(request: Request,
                username: str = Query(None)):
     con.reconnect()
     cursor = con.cursor()
     cursor.execute("SELECT id, name, username FROM member WHERE username = %s", (username, ))
     query_data = cursor.fetchone()
     print(query_data)
     if query_data:
        query_id, query_name, query_username = query_data
        member_data = {"id": query_id, "name": query_name, "username": query_username}
        return JSONResponse({"data": member_data})
     elif not request.session.get("SIGNED-IN", False): 
        return JSONResponse({"data":None})
     else:
        return JSONResponse({"data":None})

class UpdateName(BaseModel):
    name: str

@app.patch("/api/member") 
async def update(request: Request,
                 name: UpdateName): 
     name_dict = name.model_dump() # 將資料轉換為字典格式
     new_name = name_dict["name"] # 取值(新名字)
     id = request.session.get("ID")
     con.reconnect()
     cursor = con.cursor()
     cursor.execute("UPDATE member SET name = %s WHERE id = %s;", (new_name, id))
     con.commit()
     if cursor.rowcount > 0: # 獲取 SQL 操作影響的行數，確認更新是否成功
        request.session["NAME"] = new_name
        return JSONResponse({"ok": True}) # 記得大寫
     else:
        return JSONResponse({"error": True})

# 關閉資料庫連線
con.close()
