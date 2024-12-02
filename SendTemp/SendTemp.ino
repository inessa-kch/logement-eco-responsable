#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

#include "Grove_Temperature_And_Humidity_Sensor.h"

// Temp sensor definitions
#define DHTTYPE DHT11
#define DHTPIN 0
DHT dht(DHTPIN, DHTTYPE);

// Wifi connection infos
const char* ssid = "Inessa_iPhone";
const char* password = "philip15";
const char* serverName = "http://172.20.10.3:8000/mesure/";



void setup() {
  Serial.begin(115200);
  dht.begin();
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());
}




void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    WiFiClient client;
    http.begin(client, serverName);

  float temp_hum_val[2] = {0};
  if(!dht.readTempAndHumidity(temp_hum_val)) {
      Serial.print("Humidity: ");
      Serial.print(temp_hum_val[0]);
      Serial.print(" %\t");
      Serial.print("Temperature: ");
      Serial.print(temp_hum_val[1]);
      Serial.println(" *C");
  } else {
      Serial.println("Failed to get temprature and humidity value.");
      return;
  }

    String postData = "{\"id_capAct\": 1, \"valeur\": " + String(temp_hum_val[1]) + "}";
    http.addHeader("Content-Type", "application/json");

    String test = "";
    // int httpResponseCode = http.POST(test + "{\"temperature\":\"" + temp_hum_val[1] + "\"}"); 
    int httpResponseCode = http.POST(postData);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  }

  delay(3600000); // Send data every hour

}