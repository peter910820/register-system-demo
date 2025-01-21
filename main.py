import os
import psycopg2
import uvicorn

from fastapi import Cookie, FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    response = templates.TemplateResponse('login.html', {'request': request})
    response.delete_cookie("c_user")
    return response


@app.get("/regsiter", response_class=HTMLResponse)
async def root(request: Request):
    response = templates.TemplateResponse(
        'regsiter.html', {'request': request})
    return response


@app.post("/home", response_class=HTMLResponse)
async def root(request: Request, response: Response, account: str = Form(None), password: str = Form(None)):
    DATABASE_URL = os.environ['DATABASE_URL']
    database = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = database.cursor()
    print('Connect ok!')
    cursor.execute("SELECT Account, Password, Time, Date from Users")
    rows = cursor.fetchall()
    for i in range(len(rows)):
        if account == rows[i][0] and password == rows[i][1]:
            response = templates.TemplateResponse(
                'home.html', {'request': request, 'account': account})
            response.set_cookie(key="c_user", value=account)
            return response
    cursor.close()
    database.close()
    return templates.TemplateResponse('fail.html', {'request': request})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
