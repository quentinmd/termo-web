from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import csv
import os
from datetime import datetime

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

CSV_FILE = 'temperature_data.csv'

# Initialisation du fichier CSV
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', 'temperature'])

init_csv()

# Fonction pour insérer des données dans le fichier CSV
def insert_temperature(temp):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), temp])

# Fonction pour récupérer les données du fichier CSV
def get_temperature_data():
    data = []
    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            data.append(row)
    return data

temperature = 20

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    print("Ma fonction python s'execute")
    return templates.TemplateResponse("index.html", {"request": request, "temperature": temperature})

@app.get("/history", response_class=HTMLResponse)
def history(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})

@app.get("/temperature_data", response_class=JSONResponse)
def temperature_data():
    data = get_temperature_data()
    return {"data": data}

@app.post("/temperature")
async def temp_rcv(req: Request):
    global temperature

    data = await req.body()
    temperature = int(data.decode())
    insert_temperature(temperature)

    print("temperature =", temperature)

    return True

@app.get("/temperature", response_class=JSONResponse)
def get_temperature():
    global temperature
    return {"temperature": temperature}
