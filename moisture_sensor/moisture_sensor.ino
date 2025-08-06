const int mois_pin = 4;

const int airV = 3700; 
const int waterV = 910; 
int intervals = (airV - waterV) / 3;

void setup() {
	Serial.begin(115200);
	Serial.println("init esp32-s3");
	analogReadResolution(12);
	pinMode(mois_pin, INPUT);
}

void loop() {
      //Serial.print("moisture reading:");
      int raw = analogRead(mois_pin);
      //Serial.println(raw);
      if (raw > waterV && raw < (waterV + intervals))
	{  
        	Serial.println("Too wet");
      	   	delay(100);
	} 
	else if (raw  > (waterV + intervals) && raw < (airV - intervals)) 
	{
		Serial.println("Wet"); 
      	   	delay(100);
	}
	 else if (raw  < airV  && raw > (airV - intervals)) 
	{
		Serial.println("DRY!"); 
      	   	delay(100);
	}
}
