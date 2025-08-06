#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include "DFRobot_EnvironmentalSensor.h"
#include <DFRobot_SGP40.h>
#include "secrets.h"

#define I2C_ADDR 0x22          // 模块地址
#define SDA_PIN   1            // FireBeetle ESP32-S3
#define SCL_PIN   2

const int moisture_pin = 4;

WiFiClient   net;
PubSubClient client(net);
DFRobot_EnvironmentalSensor sensor(I2C_ADDR, &Wire);   // I²C 模式
DFRobot_SGP40 sgp40; // voc对象

void setup() {
  Serial.begin(115200);
  analogReadResolution(12); 
  pinMode(moisture_pin, INPUT); 
  Wire.begin(SDA_PIN, SCL_PIN);

  if (sensor.begin() != 0) {
    Serial.println("Environmental Sensor init failed!");
    while (1);
  }

  if (!sgp40.begin()) {
	Serial.println("SGP40 Not Found!!");
  }

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
 	delay(500);
	Serial.print(".");
	}
  Serial.println();
  Serial.print("WiFi connected! IP: ");
  Serial.println(WiFi.localIP());

  client.setServer(MQTT_SERVER, MQTT_PORT);
}

void loop() {
  if (!client.connected()) {
    if (client.connect("esp22-client")) Serial.println("MQTT connected");
    else { delay(200); return; }
  }

  float t   = sensor.getTemperature();          // 默认 °C
  float h   = sensor.getHumidity();             // %RH
  float p   = sensor.getAtmospherePressure();   // hPa
  float uv  = sensor.getUltravioletIntensity(); // mW/m²
  float lux = sensor.getLuminousIntensity();    // lx
  uint16_t rawVoc = sgp40.getVoclndex();     // 0-500 越大空气越操蛋
  int rawMois = map(analogRead(moisture_pin), 0, 4095, 100, 0); 

  char buf[256];
  snprintf(buf, sizeof(buf),
    "{\"Temperature\":%.2f,\"Humidity\":%.2f,\"AirPressure\":%.2f,\"UVLight\":%.2f,\"illuminance\":%.2f, \"AirCondition\": %u, \"SoilMoisture\": %d}",
    t, h, p, uv, lux, rawVoc, rawMois);

  client.publish("sensor/data", buf);
  Serial.println(buf);

  delay(100);   // 100ms 周期
}
