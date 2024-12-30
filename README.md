# IoT Home Automation System

This project is an IoT-based home automation system that allows users to monitor and control various sensors and actuators in their home. The system provides real-time data visualization and control through a web interface.

## Features

- **Real-time Monitoring**: Monitor temperature, humidity, and other environmental parameters in real-time.
- **Control Actuators**: Control devices such as lights, fans, and other appliances.
- **Data Visualization**: Visualize historical data and trends using charts.
- **Weather Forecast**: Display weather forecast data with corresponding weather conditions.

## Technologies Used

- **Backend**: FastAPI, SQLModel, SQLite
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **IoT Devices**: ESP8266, DHT11 Sensor

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/inessa-kch/logement-eco-responsable.git
    cd logement-eco-responsable
    ```

2. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the FastAPI server**:
    ```sh
    python main.py
    ```

4. **Open your browser and navigate to**:
    ```
    http://127.0.0.1:8000
    ```


## Usage

1. **Select a Logement**: Choose a logement from the dropdown or button selection.
2. **Monitor Sensors**: View real-time data from various sensors.
3. **Control Actuators**: Toggle switches to control connected devices.
4. **View Consumption Data**: Navigate to the consumption page to view historical data and trends.
5. **View Economies Realized**: Navigate to the economies page to view potential savings.


