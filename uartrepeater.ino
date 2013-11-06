int rByte = 0;
int rts = 7;

void setup(){
  pinMode(rts, OUTPUT);     
  digitalWrite(rts, HIGH);   
  
  Serial.begin(1200);
  Serial1.begin(1200);  

}


void loop(){
  if (Serial1.available() > 0) {
    while(Serial1.available()){
      rByte = Serial1.read();
      Serial.write(rByte);
    }
  }
  
  delay(1);
  
  if (Serial.available() > 0) {
    digitalWrite(rts, LOW);   
    while(Serial.available() > 0)
      Serial1.write(Serial.read()); 
    digitalWrite(rts, HIGH);
    delay(1);   
  }
}
