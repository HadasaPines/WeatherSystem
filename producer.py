from fastapi import FastAPI
import pika
import json

app = FastAPI()

@app.post("/weather/request")
def request_weather(data: dict):
    city = data.get("city")
    if not city:
        return {"error": "City is required"}

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='weather_queue')

    message = json.dumps({"city": city})
    channel.basic_publish(
        exchange='',
        routing_key='weather_queue', # שם התור אליו אנחנו שולחים את ההודעה
        body=message
    )

    connection.close()

    return {"status": "Request accepted, processing in background", "city": city}