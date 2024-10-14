from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

temperature = 15


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    print("Ma fonction python s'execute")
    return templates.TemplateResponse("index.html", {"request": request, "temperature":temperature})


@app.get("/history", response_class=HTMLResponse)
def history(request: Request):
    histo = {
        "x": [1, 2, 3, 4],
        "y": [10, 15, 23, 17],
        "type": 'scatter'
    }
    return templates.TemplateResponse("history.html", {"request": request, "histo": histo})


@app.post("/temperature")
async def temp_rcv(req: Request):
    global temperature

    data = await req.body()
    temperature = int(data.decode())

    print("temperature =", temperature)

    return True

@app.get("/temperature", response_class=JSONResponse)
def get_temperature():
    global temperature
    return {"temperature": temperature}