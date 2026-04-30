from fastapi import FastAPI
from pydantic import BaseModel, Field
import pika
import json

app = FastAPI()

class WeatherRequest(BaseModel):
    city: str = Field(..., example="City name, e.g. Tel Aviv")

@app.post("/weather/request")
def request_weather(request: WeatherRequest):
    city_name = request.city

    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
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