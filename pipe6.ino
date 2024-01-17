void pipe6() {
  //open gripper
  digitalWrite(gripperPin, LOW); 
  delay(1000);
  
  
  // move y axis forward 
  digitalWrite(dirY,HIGH);
  
  for(int x = 0; x < 442; x++) {
  
    digitalWrite(stepY,HIGH);
  
    delayMicroseconds(20000);
  
    digitalWrite(stepY,LOW);
  
    delayMicroseconds(20000);
  }
  delay(1000);

  
  digitalWrite(dirX,HIGH);
  
  for(int x = 0; x < 2710; x++) {
  
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
  
  
  // move x axis to pickup point
  digitalWrite(dirX,LOW);
  
  for(int x = 0; x < 1725; x++)  {
    digitalWrite(stepX,HIGH);
  
    delayMicroseconds(20000);
  
    digitalWrite(stepX,LOW);
  
    delayMicroseconds(20000);
    
  }
  delay(1000);
  
  
  // move y axis to pickup point
  digitalWrite(dirY,HIGH);
   
  for(int x = 0; x < 773; x++)  {
    digitalWrite(stepY,HIGH);
  
    delayMicroseconds(20000);
  
    digitalWrite(stepY,LOW);
  
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


  // move backwards to make room
  digitalWrite(dirX,LOW);
    for(int x = 0; x < 300; x++)  {
      digitalWrite(stepX,HIGH);

      delayMicroseconds(20000);

      digitalWrite(stepX,LOW);

      delayMicroseconds(20000);
    }
  delay(1000);
}
