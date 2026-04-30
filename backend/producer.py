from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pika
import json
import requests # הוספנו את זה כדי לבדוק מול שרת מזג האוויר

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "b3aa7743d0c913602cc58b3c2feb4b21"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

class WeatherRequest(BaseModel):
    city: str = Field(..., example="City name, e.g. Tel Aviv")

@app.post("/weather/request")
def request_weather(request: WeatherRequest):
    city_name = request.city

    check_url = f"{BASE_URL}?q={city_name}&appid={API_KEY}"
    response = requests.get(check_url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="City not found or invalid")

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='weather_queue')

    message = json.dumps({"city": city_name})
    channel.basic_publish(
        exchange='',
        routing_key='weather_queue',
        body=message
    )

    connection.close()

    return {"status": "Request accepted, processing in background", "city": city_name}