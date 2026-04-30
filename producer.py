from fastapi import FastAPI
import pika
import json

app = FastAPI()

@app.post("/weather/request")
def request_weather(data: dict):
    city = data.get("city")
    if not city:
        return {"error": "City is required"}

    # 1. התחברות לשרת ה-RabbitMQ שלנו שרץ בדוקר
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # 2. מוודאים שהתור קיים (אם לא, הוא ייווצר אוטומטית)
    channel.queue_declare(queue='weather_queue')

    # 3. אריזת הנתונים לפורמט טקסטואלי (JSON) ושליחתם לתור
    message = json.dumps({"city": city})
    channel.basic_publish(
        exchange='',
        routing_key='weather_queue', # שם התור אליו אנחנו שולחים את ההודעה
        body=message
    )

    # 4. סגירת החיבור ל-RabbitMQ בצורה מסודרת
    connection.close()

    # 5. החזרת תשובה מיידית למשתמש, מבלי לחכות לעיבוד
    return {"status": "Request accepted, processing in background", "city": city}