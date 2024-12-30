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
    git clone https://github.com/yourusername/iot-home-automation.git
    cd iot-home-automation
    ```

2. **Create a virtual environment and activate it**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the FastAPI server**:
    ```sh
    uvicorn main:app --reload
    ```

5. **Open your browser and navigate to**:
    ```
    http://127.0.0.1:8000
    ```

## Project Structure
.
├── main.py                     # Main application file
├── models.py                   # Database models
├── templates/
│   ├── base.html               # Base HTML template
│   ├── index.html              # Home page template
│   ├── etat.html               # Sensor/Actuator status page
│   ├── consommation.html       # Consumption data visualization page
│   ├── economies.html          # Economies realized visualization page
├── static/
│   ├── css/
│   │   ├── styles.css          # Main stylesheet
│   │   ├── economies.css       # Economies page stylesheet
│   ├── js/
│   │   ├── etat.js             # JavaScript for sensor/actuator status page
│   │   ├── consommation.js     # JavaScript for consumption data visualization
│   │   ├── economies.js        # JavaScript for economies realized visualization
├── SendTemp/
│   ├── SendTemp.ino            # Arduino code for sending temperature and humidity data
├── logement.sql                # SQL script for creating and populating the database
├── requirements.txt            # Python dependencies
└── README.md                   # Project README file



## Usage

1. **Select a Logement**: Choose a logement from the dropdown or button selection.
2. **Monitor Sensors**: View real-time data from various sensors.
3. **Control Actuators**: Toggle switches to control connected devices.
4. **View Consumption Data**: Navigate to the consumption page to view historical data and trends.
5. **View Economies Realized**: Navigate to the economies page to view potential savings.


