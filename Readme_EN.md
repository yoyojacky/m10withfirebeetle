# UNIHIKER M10 meets FireBeetle ESP32-S3

## Project Overview

This project uses the UNIHIKER M10 as the core control unit to acquire data from multiple sensors connected to a remote ESP32-S3 device via MQTT protocol. The sensors include a soil moisture sensor, a DFRobot Gravity Multifunctional Environmental Sensor, and an air quality sensor. The acquired data is rendered in real-time as line charts to intuitively display sensor status information. When the air quality sensor detects deteriorating air quality, the system plays alert messages through a TTS (Text-to-Speech) module connected to the UNIHIKER M10 to remind users to take appropriate measures.

## Hardware Components

- **UNIHIKER M10**: Serves as the main control device of the project, responsible for receiving sensor data, processing data, and controlling the TTS module to play alert messages.
- **ESP32-S3**: Edge device that connects various sensors and transmits sensor data to the UNIHIKER M10 over Wi-Fi.
- **Sensors**:
  - **Soil Moisture Sensor**: Used to detect soil moisture levels, suitable for agriculture, horticulture, and other fields. It helps users understand plant growth environments.
  - **DFRobot Gravity Multifunctional Environmental Sensor**: Can simultaneously measure multiple environmental parameters such as temperature, humidity, barometric pressure, light intensity, and UV intensity, providing users with comprehensive environmental information.
  - **Air Quality Sensor**: Used to monitor air quality. When deteriorating air quality is detected, it triggers the voice alarm function.
- **TTS Module**: Connected to the UNIHIKER M10, used to play alert messages and remind users of air quality issues.

## Software Components

- **MQTT Protocol**: Used to achieve data communication between ESP32-S3 and UNIHIKER M10. The ESP32-S3 acts as a client and publishes collected sensor data to the UNIHIKER M10 through the MQTT protocol.
- **Data Processing and Visualization**: After receiving data, the UNIHIKER M10 processes the data and intuitively displays sensor status information through real-time rendered line charts. The line charts clearly reflect the changing trends of sensor data over time, allowing users to quickly understand the current environmental conditions.
- **Voice Alarm Function**: When the air quality sensor detects deteriorating air quality, the UNIHIKER M10 triggers the TTS module to play preset alert messages, reminding users to take appropriate measures such as ventilation.

## Implementation Principles

### Data Acquisition

1. The ESP32-S3 device connects to the soil moisture sensor, DFRobot Gravity Multifunctional Environmental Sensor, and air quality sensor, periodically collecting data from each sensor.
2. The ESP32-S3 connects to the network over Wi-Fi and acts as an MQTT client, encapsulating the collected sensor data into MQTT messages and publishing them to the configured MQTT broker (with the UNIHIKER M10 as the broker or forwarded through an intermediate MQTT broker).

### Data Transmission and Reception

1. The UNIHIKER M10 runs an MQTT client program, subscribing to the sensor data topic published by the ESP32-S3.
2. When the UNIHIKER M10 receives MQTT messages, it parses the message content and extracts the sensor data.

### Data Processing and Visualization

1. The UNIHIKER M10 processes the received sensor data, stores the data, and updates the data queue.
2. Graphics libraries (such as uGUI, etc.) are used for real-time rendering of line charts, displaying sensor data in curve form on the display screen. The horizontal axis of the line chart represents time, and the vertical axis represents sensor data values. By dynamically updating the line charts, users can intuitively see the changing trends of each sensor data.

### Voice Alarm Function

1. The UNIHIKER M10 monitors the air quality sensor data in real-time. When it detects that air quality is below the preset threshold, it triggers the voice alarm function.
2. The UNIHIKER M10 controls the connected TTS module to play preset alert voice messages, reminding users that air quality has deteriorated and they need to take appropriate measures.

## Key Features

- **Real-time Performance**: Data is quickly transmitted through the MQTT protocol, ensuring sensor data can be updated in real-time and displayed on line charts, allowing users to promptly understand environmental changes.
- **Intuitiveness**: Sensor data is displayed using line charts, which is intuitive and easy to understand, enabling users to quickly judge current environmental conditions.
- **Alarm Function**: When air quality deteriorates, the voice alarm function can promptly remind users, enhancing the project's practicality and safety.
- **Scalability**: Based on the MQTT protocol and UNIHIKER M10 architecture, more sensors or other functional modules can be easily added to meet the needs of different scenarios.

## Application Scenarios

This project is suitable for various scenarios, such as smart home environmental monitoring, agricultural greenhouse environmental monitoring, small-scale weather stations, and more. By real-time monitoring of environmental parameters and timely alerts, it provides users with convenient environmental management solutions, helping users better understand and manage their surrounding environment.

## Development Environment

- Raspberry Pi 5 + arduino-cli + ESP32-S3 + Gravity Multifunctional Environmental Sensor V2.0
- **ESP32 Code**: Located in `esp32_weather`
- **UNIHIKER M10 Code**: Located in `M10-python-code`

## Code Upload Method

1. Connect UNIHIKER M10 to USB and wait for it to start.
2. Use mobaXterm to establish a remote connection to 10.1.2.3:

```bash
ssh root@10.1.2.3
```

Password by default: dfrobot

3. Navigate to the `/opt/unihiker/examples/` directory and create your project directory:

```bash
mkdir 12-yoyojacky
cd 12-yoyojacky
```

4. Copy the code from the repository into the directory. Modify the IP address and port number information according to your actual situation.
   You can also modify the code content as needed to adapt to your actual environment.

## Note

The entire operation is compiled and uploaded via arduino-cli. For specific details, please refer to topics related to `arduino-cli`.
