/*
  I2C Scanner
  运行后串口会打印所有应答设备的地址（7 位格式）。
*/

#include <Wire.h>

void setup() {
  Serial.begin(115200);
  // ESP32-S3 示例：SDA=18，SCL=17
  Wire.begin(1, 2);

  Serial.println("\nI2C Scanner");
}

void loop() {
  byte nDevices = 0;
  Serial.println("Scanning...");

  for (byte address = 1; address < 127; ++address) {
    Wire.beginTransmission(address);
    byte error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("I2C device found at 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
      nDevices++;
    } else if (error == 4) {
      Serial.print("Unknown error at 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
    }
  }

  if (nDevices == 0)
    Serial.println("No I2C devices found\n");
  else
    Serial.println("done\n");

  delay(2000);   // 每 2 秒扫一次
}
