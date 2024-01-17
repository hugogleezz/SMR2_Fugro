void pipe3back() {
  //open gripper
  digitalWrite(gripperPin, LOW); 
  delay(1000);


  // move y axis to pickup point
  digitalWrite(dirY,HIGH);
   
  for(int x = 0; x < 1215; x++)  {
    digitalWrite(stepY,HIGH);
  
    delayMicroseconds(20000);
  
    digitalWrite(stepY,LOW);
  
    delayMicroseconds(20000);
  }
  delay(1000);
  
  
  // move x axis forward to pickup
  digitalWrite(dirX,HIGH);
  
  for(int x = 0; x < 985; x++) {
  
    digitalWrite(stepX,HIGH);
  
    delayMicroseconds(20000);
  
    digitalWrite(stepX,LOW);
  
    delayMicroseconds(20000);
  }
  delay(1000);

  
  // close gripper
  digitalWrite(gripperPin, HIGH); 
  delay(1000);
  
  
  // move z axis up
  digitalWrite(dirZ,LOW);
  
  for(int x = 0; x < 250; x++)  {
    digitalWrite(stepZ,HIGH);
  
    delayMicroseconds(20000);
  
    digitalWrite(stepZ,LOW);
  
    delayMicroseconds(20000);
  }
  delay(1000);

    // move y axis to 1 row
  digitalWrite(dirY,LOW);
   
  for(int x = 0; x < 1215; x++)  {
    digitalWrite(stepY,HIGH);
  
    delayMicroseconds(20000);
  
    digitalWrite(stepY,LOW);
  
    delayMicroseconds(20000);
  }
  delay(1000);

    // move x axis to 3
  digitalWrite(dirX,HIGH);
  
  for(int x = 0; x < 1725; x++)  {
    digitalWrite(stepX,HIGH);
  
    delayMicroseconds(20000);
  
    digitalWrite(stepX,LOW);
  
    delayMicroseconds(20000);
    
  }
  delay(1000);


  // move z axis down
  digitalWrite(dirZ,HIGH);
  
  for(int x = 0; x < 250; x++)  {
    digitalWrite(stepZ,HIGH);
  
    delayMicroseconds(20000);
  
    digitalWrite(stepZ,LOW);
  
    delayMicroseconds(20000);
  }
  delay(1000);

  // open gripper
  digitalWrite(gripperPin, LOW); 
  delay(1000);

}
  
