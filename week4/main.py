from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI() #FastAPI 物件: FastAPI 框架下最核心物件

templates = Jinja2Templates(directory="templates") #uvicorn main:app --reload
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="secret_key") 


@app.get("/") # get會把要傳送的值放在header上，直接顯示在URL，不適合傳輸隱密資料
async def homepage(request: Request):
    return templates.TemplateResponse(
        "home.html", {"request": request, "title": "歡迎光臨，請輸入帳號密碼"})

@app.post("/signin") 
async def login(request: Request,
    # 讓參數變成非必選, 解決 422 unprocessable entity 問題
    text: str = Form(None), # None 作為默認值傳遞給參數，故若無提供參數為 None (若有提供參數會是 string 型態)
    password: str = Form(None)):
    if text is None or password is None: # 無參數的狀況下
        return RedirectResponse(url="/error?message=請輸入帳號、密碼", status_code=302)
    if text == "test" and password == "test":
        request.session["SIGNED-IN"] = True # 在 request.session 字典中設定名為 "SIGNED-IN" 的 key，其 Value = True
        return RedirectResponse(url="/member", status_code=302) # code 默認為 307，重定向時保留原 HTTP 方法和數據 (post仍為post)，而 302 post 則可變 get
    else:
        return RedirectResponse(url="/error?message=帳號、密碼輸入錯誤", status_code=302)

@app.get("/member") 
async def member(request: Request):
    # 從 request 中獲取名為 "SIGNED-IN" 的 key，若 key 存在則返回其值，不存在則返回 False
    # if not = 若 "SIGNED-IN" 不存在 or 值 = False >> 表示未登入
    if not request.session.get("SIGNED-IN", False): 
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(
        "success.html", {"request": request, "title": "歡迎光臨，這是會員頁", "message": "恭喜您，成功登入系統", "redirect":"登出系統"})

@app.get("/error") 
async def error(request: Request, message: str = "請輸入帳號、密碼"):
    return templates.TemplateResponse(
        "error.html", {"request": request, "title": "失敗頁面", "message": message, "redirect": "返回頁面"})
@app.get("/error") 
async def error(request: Request, message: str = "帳號、密碼輸入錯誤"):
    return templates.TemplateResponse(
        "error.html", {"request": request, "title": "失敗頁面", "message": message, "redirect": "返回頁面"})

@app.get("/signout") 
async def login(request: Request):
    request.session["SIGNED-IN"] = False
    return RedirectResponse(url="/", status_code=302)