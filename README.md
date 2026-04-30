# Weather System with RabbitMQ & Docker 🌤️

A robust, microservices-based weather application built with Python and FastAPI. The system demonstrates asynchronous message processing using RabbitMQ and integrates with a real-world external API.

## 🏗️ Project Architecture

The system consists of four main components running in separate Docker containers:

1. **Producer (API 1):** A FastAPI server that receives weather requests for a specific city from the user and pushes the task into a RabbitMQ message queue.
2. **RabbitMQ Message Broker:** Manages the `weather_queue`, ensuring messages are held safely until a consumer is ready to process them.
3. **Consumer (API 2 & Worker):** A background worker that pulls messages from the queue, fetches real-time weather data using the **OpenWeatherMap API**, and saves the results in-memory. It also exposes a FastAPI endpoint to retrieve the processed results.
4. **Frontend (UI):** A modern React user interface that interacts with the backend APIs to provide a seamless visual experience for adding tasks and viewing results.

## 🚀 Technologies Used
* **React & Vite** (Frontend UI)
* **Python 3.11**
* **FastAPI** & **Uvicorn** (for RESTful APIs)
* **RabbitMQ** (Message Broker)
* **Pika** (Python RabbitMQ client)
* **Requests** (For external API calls)
* **Docker & Docker Compose** (Containerization and orchestration)

## 📋 Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running on your machine.

## 🛠️ How to Run the Project

You don't need to install Python, Node.js, or any dependencies locally. Docker will handle everything for you.

1. Clone this repository to your local machine:
   ```bash
   git clone [https://github.com/HadasaPines/WeatherSystem.git](https://github.com/HadasaPines/WeatherSystem.git)
   cd WeatherSystem
   ```

2. Start the system using Docker Compose:
   ```bash
   docker compose up --build
   ```

3. Wait a few seconds for the application to start completely. You will see logs indicating that the Uvicorn servers, the React frontend, and RabbitMQ are running. The Consumer is configured to wait and retry connecting until RabbitMQ is fully ready.

## 📝 How to View Logs (Terminal Prints)

Once the system is running, you can monitor the internal processes (like message consumption and external API calls) by checking the logs. There are two ways to do this:

1. **Directly in the Terminal:** 
   If you ran `docker compose up --build`, the terminal will display color-coded logs for all services in real-time. Look for the `consumer` lines to see when messages are processed.
2. **Via Docker Desktop (Recommended):**
   * Open Docker Desktop and go to the **Containers** tab.
   * Click on the project name (e.g., `weathersystem`).
   * Go to the **Logs** tab. You can filter the logs by selecting a specific service (like `consumer`) on the left side to see its specific prints clearly.

## 🌐 Endpoints & Usage

Once the containers are up, you have multiple ways to interact with the system:

### 1. Visual Dashboard (Frontend UI) - ⭐ Recommended
* **URL:** [http://localhost:5173](http://localhost:5173)
* **Action:** Open this link in your browser to interact with the system visually.
* *Features:* You can add cities to the processing queue (⏳), get instant validation for invalid cities, watch the status change to ready (✅), and fetch cached results seamlessly.

### 2. Request Weather via API (Producer)
* **URL:** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Action:** Send a `POST` request to `/weather/request` with the following JSON body:
  ```json
  {
    "city": "London"
  }
  ```
* *This will send the request to the RabbitMQ queue.*

### 3. Get Results via API (Consumer/Result API)
* **URL:** [http://localhost:8001/docs](http://localhost:8001/docs)
* **Action:** Send a `GET` request to `/weather/result` with the city name (e.g., `London`).
* *This will return the real-time weather data fetched by the background worker.*

### 4. RabbitMQ Management Dashboard
* **URL:** [http://localhost:15672](http://localhost:15672)
* **Login:** Username: `guest` | Password: `guest`
* *Use this dashboard to monitor the queues, connections, and message flow in real-time.*

## 🛑 Stopping the System
To stop the running containers, simply press `Ctrl+C` in the terminal where Docker is running, or run the following command in a new terminal:
```bash
docker compose down
```