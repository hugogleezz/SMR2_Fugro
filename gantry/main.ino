// defines pins numbers
int currentState = 1;

int mainCounterX = 0;  // Counter for triggerPinX
int mainCounterY = 0;  // Counter for triggerPinY

bool keepRunning = true;

const int gripperPin = 9;
const int triggerPinX = 12;
const int triggerPinY = 13;

const int stepX = 2;
const int dirX  = 5;

const int stepY = 3;
const int dirY  = 6;

const int stepZ = 4;
const int dirZ  = 7;

const int enPin = 8;

void setup() {
  Serial.begin(9600);
  // Sets the two pins as Outputs
  pinMode(stepX, OUTPUT);
  pinMode(dirX, OUTPUT);
  pinMode(stepY, OUTPUT);
  pinMode(dirY, OUTPUT);
  pinMode(stepZ, OUTPUT);
  pinMode(dirZ, OUTPUT);
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);
  pinMode(triggerPinX, INPUT);
  pinMode(triggerPinY, INPUT);
  pinMode(gripperPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    Serial.println(command);

    if (command == "1") {
      Serial.print("picking pipe");
      pipe1();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "2") {
      Serial.print("picking pipe");
      pipe2();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "3") {
      Serial.print("picking pipe");
      pipe3();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "4") {
      Serial.print("picking pipe");
      pipe4();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "5") {
      Serial.print("picking pipe");
      pipe5();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "6") {
      Serial.print("picking pipe");
      pipe6();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "7") {
      Serial.print("picking pipe");
      pipe7();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "8") {
      Serial.print("picking pipe");
      pipe8();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "9") {
      Serial.print("picking pipe");
      pipe9();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "1B") {
      Serial.print("putting back pipe");
      pipe1back();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "2B") {
      Serial.print("putting back pipe");
      pipe2back();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "3B") {
      Serial.print("putting back pipe");
      pipe3back();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "4B") {
      Serial.print("putting back pipe");
      pipe4back();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "5B") {
      Serial.print("putting back pipe");
      pipe5back();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "6B") {
      Serial.print("putting back pipe");
      pipe6back();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "7B") {
      Serial.print("putting back pipe");
      pipe7back();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "8B") {
      Serial.print("putting back pipe");
      pipe8back();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    } else if (command == "9B") {
      Serial.print("putting back pipe");
      pipe9back();
      Serial.print("pipe is picked");
      limitXY();
      //Serial.print("Done");
    }


}
}

void limitXY() {
  digitalWrite(dirX, LOW);
  digitalWrite(dirY, LOW);
  
  while (keepRunning == true){
    // Check if the trigger pin for X is LOW
    if (digitalRead(triggerPinX) == LOW) {
      // Stop the motor for X
      digitalWrite(stepX, LOW);
      mainCounterX++; // Increment the counter for triggerPinX
    } else {
      // Motor X is running if trigger pin is HIGH and the control variable is true
      if (keepRunning) {
        // Assuming stepX is the pin connected to the stepper motor X
        digitalWrite(stepX, HIGH);
        delayMicroseconds(20000); // Adjust delay as needed
        digitalWrite(stepX, LOW);
        delayMicroseconds(20000); // Adjust delay as needed
        // Other loop code for X, if any
        // Perform additional actions for X here
      }
    }
  
   
  
    // Check if the trigger pin for Y is LOW
    if (digitalRead(triggerPinY) == LOW) {
      // Stop the motor for Y
      digitalWrite(stepY, LOW);
      mainCounterY++; // Increment the counter for triggerPinY
    } else {
      // Motor Y is running if trigger pin is HIGH and the control variable is true
      if (keepRunning) {
        // Assuming stepY is the pin connected to the stepper motor Y
        digitalWrite(stepY, HIGH);
        delayMicroseconds(20000); // Adjust delay as needed
        digitalWrite(stepY, LOW);
        delayMicroseconds(20000); // Adjust delay as needed
        // Other loop code for Y, if any
        // Perform additional actions for Y here
      }
    }
  
    // Check if both trigger pins are low, and shut off the system if true
    if (mainCounterX > 0 && mainCounterY > 0) {
      keepRunning = false;
    }  
  }
  mainCounterX = 0;
  mainCounterY = 0;
  keepRunning = true;
}
