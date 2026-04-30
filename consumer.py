import pika
import json
import threading
import time
from fastapi import FastAPI

app = FastAPI()

weather_results = {}

def consume_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='weather_queue')

    def callback(ch, method, properties, body):
        data = json.loads(body)
        city = data.get("city")
        print(f"\n[x] Received request for {city}, processing...")
        
        time.sleep(5)
        
        weather_results[city] = {
            "temperature": 24,
            "condition": "Sunny"
        }
        print(f"[v] Finished processing {city}. Data saved in memory.")

    channel.basic_consume(queue='weather_queue', on_message_callback=callback, auto_ack=True)
    print("\n [*] Consumer is waiting for messages...")
    channel.start_consuming()

threading.Thread(target=consume_messages, daemon=True).start()


@app.get("/weather/result")
def get_weather_result(city: str):
    result = weather_results.get(city)
    
    if result:
        return {"city": city, "weather": result}
    else:
        return {"city": city, "message": "Result pending or city not found"}