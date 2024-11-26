# -*- coding: utf-8 -*-
from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import extension
import environment

__author__ = 'lcy'


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")  # 挂载静态文件
templates = Jinja2Templates(directory="templates")  # 创建一个templates（模板）对象，templates可以重用。


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result_dict": None})

@app.get("/refresh", response_class=HTMLResponse)
async def read_root_post(request: Request):
    environment.refresh_cookies()
    return templates.TemplateResponse("index.html", {"request": request, "refresh": "刷新cookies成功~"})


@app.post("/uploader/", response_class=HTMLResponse)
async def create_upload_file(request: Request, file: UploadFile = File(...)):
    # 检查文件扩展名
    if not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="Only .md files are allowed")
    contents = await file.read()
    result_dict = await extension.crawlers_start(file_name=file.filename, md_content=contents.decode("utf-8"))
    return templates.TemplateResponse("index.html", {"request": request, "result_dict": result_dict})


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
