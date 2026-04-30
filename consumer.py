import pika
import json
import threading
import requests
from fastapi import FastAPI
import time

app = FastAPI()

weather_results = {}

API_KEY = "b3aa7743d0c913602cc58b3c2feb4b21" 
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def consume_messages():
    connection = None
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            print("\n[+] Successfully connected to RabbitMQ!")
            break  
        except pika.exceptions.AMQPConnectionError:
            print("\n[!] RabbitMQ is not ready yet, waiting 3 seconds...")
            time.sleep(3) 

    channel = connection.channel()
    channel.queue_declare(queue='weather_queue')

    def callback(ch, method, properties, body):
        data = json.loads(body)
        city = data.get("city")
        print(f"\n[x] Received request for {city}, fetching REAL weather...")
        time.sleep(3)
        try:
            complete_url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
            
            response = requests.get(complete_url)
            weather_data = response.json()

            if response.status_code == 200:
                temp = weather_data["main"]["temp"]
                condition = weather_data["weather"][0]["main"]
                
                weather_results[city] = {
                    "temperature": temp,
                    "condition": condition,
                    "status": "Success"
                }
                print(f"[v] Success! {city}: {temp}°C, {condition}")
            
            else:
                error_msg = weather_data.get("message", "Unknown error")
                weather_results[city] = {
                    "status": "Failed",
                    "error": error_msg
                }
                print(f"[x] Failed to find weather for {city}. Error: {error_msg}")

        except Exception as e:
            weather_results[city] = {"status": "Failed", "error": "Network Error"}
            print(f"[!] Exception processing {city}: {str(e)}")

    channel.basic_consume(queue='weather_queue', on_message_callback=callback, auto_ack=True)
    print("\n [*] Consumer is waiting for messages...")
    channel.start_consuming()

threading.Thread(target=consume_messages, daemon=True).start()

@app.get("/weather/result")
def get_weather_result(city: str):
    result = weather_results.get(city)
    if result:
        return {"city": city, "data": result}
    else:
        return {"city": city, "message": "Result pending or city not found"}