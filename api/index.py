from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
from datetime import datetime
import os

app = FastAPI(
    title="United Airlines Flight Difficulty Dashboard",
    description="Real-time analysis of United Airlines flight operations and difficulty patterns",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

SAMPLE_DATA = {
    "total_flights": 8155,
    "avg_delay": 6.8,
    "delayed_pct": 34.8,
    "avg_difficulty": 0.752,
    "difficulty_distribution": {
        "Easy": 4083,
        "Medium": 2446,
        "Difficult": 1626
    },
    "destinations": [
        {"dest": "YYZ", "difficult": 77, "score": 0.89, "delay": 23.4},
        {"dest": "STL", "difficult": 53, "score": 0.85, "delay": 19.8},
        {"dest": "LHR", "difficult": 44, "score": 0.92, "delay": 28.1},
        {"dest": "YOW", "difficult": 41, "score": 0.87, "delay": 21.5},
        {"dest": "YUL", "difficult": 39, "score": 0.83, "delay": 18.9},
        {"dest": "DEN", "difficult": 31, "score": 0.78, "delay": 15.2},
        {"dest": "SEA", "difficult": 28, "score": 0.74, "delay": 13.8},
        {"dest": "LAX", "difficult": 25, "score": 0.71, "delay": 12.5},
        {"dest": "SFO", "difficult": 22, "score": 0.69, "delay": 11.3},
        {"dest": "ATL", "difficult": 19, "score": 0.67, "delay": 10.1}
    ],
    "fleet": [
        {"type": "B787", "difficult": 156, "score": 0.89, "passengers": 241},
        {"type": "B767", "difficult": 134, "score": 0.87, "passengers": 216},
        {"type": "B757", "difficult": 98, "score": 0.82, "passengers": 186},
        {"type": "B738", "difficult": 87, "score": 0.79, "passengers": 162},
        {"type": "B737", "difficult": 65, "score": 0.75, "passengers": 148},
        {"type": "A319", "difficult": 43, "score": 0.71, "passengers": 126}
    ],
    "time_data": [
        {"hour": 6, "difficult": 45, "delay": 8.2},
        {"hour": 7, "difficult": 78, "delay": 12.5},
        {"hour": 8, "difficult": 125, "delay": 18.3},
        {"hour": 9, "difficult": 167, "delay": 22.1},
        {"hour": 10, "difficult": 143, "delay": 19.7},
        {"hour": 11, "difficult": 98, "delay": 14.2},
        {"hour": 12, "difficult": 87, "delay": 12.8},
        {"hour": 13, "difficult": 76, "delay": 11.5},
        {"hour": 14, "difficult": 89, "delay": 13.1},
        {"hour": 15, "difficult": 134, "delay": 16.8},
        {"hour": 16, "difficult": 167, "delay": 20.3},
        {"hour": 17, "difficult": 189, "delay": 24.1},
        {"hour": 18, "difficult": 156, "delay": 21.7},
        {"hour": 19, "difficult": 123, "delay": 18.5},
        {"hour": 20, "difficult": 87, "delay": 13.9},
        {"hour": 21, "difficult": 65, "delay": 10.2},
        {"hour": 22, "difficult": 43, "delay": 7.8},
        {"hour": 23, "difficult": 32, "delay": 6.1}
    ]
}

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):

    return  + json.dumps(SAMPLE_DATA["destinations"][:8]) +  + json.dumps(SAMPLE_DATA["fleet"]) +
    return {
        "total_flights": SAMPLE_DATA["total_flights"],
        "avg_delay": SAMPLE_DATA["avg_delay"],
        "delayed_pct": SAMPLE_DATA["delayed_pct"],
        "avg_difficulty": SAMPLE_DATA["avg_difficulty"],
        "difficulty_distribution": SAMPLE_DATA["difficulty_distribution"]
    }

@app.get("/api/destinations")
async def get_destinations():

    return SAMPLE_DATA["destinations"]

@app.get("/api/fleet")
async def get_fleet():

    return SAMPLE_DATA["fleet"]

@app.get("/api/time-data")
async def get_time_data():

    return SAMPLE_DATA["time_data"]

@app.get("/api/health")
async def health_check():

    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'framework': 'FastAPI',
        'version': '1.0.0',
        'deployed': 'Vercel',
        'sample_data': True
    }

@app.get("/demo")
async def demo():

    return

app_instance = app

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting United Airlines Flight Difficulty Dashboard (FastAPI)")
    print("📊 Serving sample data (no heavy dependencies)")
    print("🌐 Dashboard will be available at: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)