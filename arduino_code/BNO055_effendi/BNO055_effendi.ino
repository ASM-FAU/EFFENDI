#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
#include <EEPROM.h>
  
Adafruit_BNO055 bno = Adafruit_BNO055(70, 0x28);


//The current readings from the FSRs, A stands for Analog Input
int fsrThumbLeft; //A7 
int fsrIndexLeft; //A8 
int fsrMiddleLeft; //A9 
int fsrRingLeft; //A10 
int fsrLittleLeft; //A11

int fsrTemporalLeft; //A6
int fsrTemporalRight; //A5

int fsrThumbRight; //A4
int fsrIndexRight; //A3
int fsrMiddleRight; //A2
int fsrRingRight; //A1
int fsrLittleRight; //A0

int fsrVoltage0;
int fsrVoltage1;

float yaw;
float roll;
float pitch;
float yaw_pre;
float yaw_filtered;
float pitch_pre;
float pitch_filtered;
float roll_pre;
float roll_filtered;
float oldDataYaw;
float oldDataPitch;
float oldDataRoll;

int incomingByte;

// The pin numbers for the RGB LED
int redPin = 6;
int greenPin = 4;
int bluePin = 5;

const int vibMotor1 = 13;
int vibMotor2 = 12;
int motorState1 = LOW;
int motorState2 = LOW;

float filter_degree = 0.0;  // was 0.8
float sensor_tolerance = 0.1; // was 0.04

unsigned long previousMillis = 0; // will store last time the motor state was updated
const long interval = 100; // number of millisecs that Motor's are on - all two motors use this


void setup(void) 
{
  Serial.begin(115200);
  Serial.println("Orientation Sensor Test"); Serial.println("");
//  BNO055_OPR_MODE_ADDR = 0000x0101b
//  OPR_MODE =

  //bno.setMode(bno.OPERATION_MODE_IMUPLUS);
  //bno.begin(bno.OPERATION_MODE_IMUPLUS);
  bno.begin(bno.OPERATION_MODE_CONFIG);
  
  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  // configure LED and Vibration Motor Pins as output
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT); 
  pinMode(vibMotor1, OUTPUT);
  pinMode(vibMotor2, OUTPUT);

  // Load calibration data from EEPROM
  int eeAddress = 0;
  long bnoID;
  bool foundCalib = false;

  EEPROM.get(eeAddress, bnoID);

  adafruit_bno055_offsets_t calibrationData;
  sensor_t sensor;

  /*
  *  Look for the sensor's unique ID at the beginning oF EEPROM.
  *  This isn't foolproof, but it's better than nothing.
  */
  bno.getSensor(&sensor);
  if (bnoID != sensor.sensor_id)
  {
      Serial.println("\nNo Calibration Data for this sensor exists in EEPROM");
      setColor(255, 0, 0);
      delay(500);
  }
  else
  {
      Serial.println("\nFound Calibration for this sensor in EEPROM.");
      eeAddress += sizeof(long);
      EEPROM.get(eeAddress, calibrationData);

      Serial.println("\n\nRestoring Calibration data to the BNO055...");
      bno.setSensorOffsets(calibrationData);

      Serial.println("\n\nCalibration data loaded into BNO055");
      foundCalib = true;
      //setColor(0, 255, 255);
      setColor(255, 0, 255);
  }

  //setColor(0, 0, 255);
  bno.begin(bno.OPERATION_MODE_IMUPLUS);
  //bno.begin(bno.OPERATION_MODE_NDOF);
  delay(1000);

  /* Crystal must be configured AFTER loading calibration data into BNO055. */
  bno.setExtCrystalUse(true);

  sensors_event_t event;
  bno.getEvent(&event);
  /* always recal the mag as It goes out of calibration very often */
  if (foundCalib){
      Serial.println("Move sensor slightly to calibrate magnetometers");
      //while (!bno.isFullyCalibrated())
      uint8_t system, gyro, accel, mag;
      system = gyro = accel = mag = 0;
      bno.getCalibration(&system, &gyro, &accel, &mag);

      while (gyro == 3 && accel == 3 && mag == 3)
      {
          bno.getEvent(&event);
          delay(100);
      }
      setColor(0, 0, 255);
  }

  // optional?
  Serial.println("\nFully calibrated!");
  Serial.println("--------------------------------");
  adafruit_bno055_offsets_t newCalib;
  bno.getSensorOffsets(newCalib);

//  Serial.println("\n\nStoring calibration data to EEPROM...");
//
//  eeAddress = 0;
//  bno.getSensor(&sensor);
//  bnoID = sensor.sensor_id;
//
//  EEPROM.put(eeAddress, bnoID);
//
//  eeAddress += sizeof(long);
//  EEPROM.put(eeAddress, newCalib);
//  Serial.println("Data stored to EEPROM.");

  Serial.println("\n--------------------------------\n");
  delay(500);
    
  //bno.setExtCrystalUse(true);
}

void loop(void) 
{
  // setup FSR sensors to analog Pins
  fsrLittleRight = analogRead(0);
  fsrRingRight = analogRead(1);
  fsrMiddleRight = analogRead(2);
  fsrIndexRight = analogRead(3);
  fsrThumbRight = analogRead(4);
  
  fsrTemporalRight = analogRead(5);
  fsrTemporalLeft = analogRead(6);
  
  fsrThumbLeft = analogRead(7);
  fsrIndexLeft = analogRead(8);
  fsrMiddleLeft = analogRead(9); 
  fsrRingLeft = analogRead(10);
  fsrLittleLeft = analogRead(11);

  
  /* Get a new sensor event */ 
  sensors_event_t event; 
  //bno.getEvent(&event, Adafruit_BNO055::VECTOR_EULER);
  bno.getEvent(&event);
  
  // Get data from the IMU
  if (event.orientation.x > 180.){
    yaw = event.orientation.x - 360.;
  } else {
    yaw = event.orientation.x;
  }
  roll = event.orientation.z;
  pitch = event.orientation.y;

  // Filter data
//  yaw_pre = yaw_filtered;
//  yaw_filtered = (1-filter_degree) * yaw + filter_degree * yaw_pre;
//  if(abs(oldDataYaw - yaw_filtered) <= sensor_tolerance){
//    yaw_filtered = oldDataYaw;
//  }
//  oldDataYaw = yaw_filtered;

//  roll_pre = roll_filtered;
//  roll_filtered = (1-filter_degree) * roll + filter_degree * roll_pre;
//  if(abs(oldDataRoll - roll_filtered) <= sensor_tolerance){
//    roll_filtered = oldDataRoll;
//  }
//  oldDataRoll = roll_filtered;

//  pitch_pre = pitch_filtered;
//  pitch_filtered = (1-filter_degree) * pitch + filter_degree * pitch_pre;
//  if(abs(oldDataPitch - pitch_filtered) <= sensor_tolerance){
//    pitch_filtered = oldDataPitch;
//  }
//  oldDataPitch = pitch_filtered;

  yaw_filtered = yaw;
  roll_filtered = roll;
  pitch_filtered = pitch;
  

  // Output data to main program
  Serial.print(yaw_filtered); //coordinate[0]
  Serial.print(",");
  Serial.print(pitch_filtered); //coordinate[1]
  Serial.print(",");
  Serial.print(roll_filtered); //coordinate[14] for scrolling
  Serial.print(",");

  Serial.print(fsrTemporalRight); //Click Value //coordinate[2]
  Serial.print(",");
  Serial.print(fsrTemporalLeft); //Click Value //coordinate[3]
  Serial.print(",");
  
  Serial.print(fsrLittleLeft); //coordinate[4] button0
  Serial.print(",");
  Serial.print(fsrRingLeft); //coordinate[5] button1
  Serial.print(",");
  Serial.print(fsrMiddleLeft); //coordinate[6] button2
  Serial.print(",");
  Serial.print(fsrIndexLeft); //coordinate[7] button3
  Serial.print(",");
  Serial.print(fsrThumbLeft); //coordinate[8] button4
  Serial.print(",");
  
  Serial.print(fsrThumbRight); //coordinate[9] button5
  Serial.print(",");
  Serial.print(fsrIndexRight); //coordinate[10] button6
  Serial.print(",");
  Serial.print(fsrMiddleRight); //coordinate[11] button7
  Serial.print(",");
  Serial.print(fsrRingRight); //coordinate[12] button8
  Serial.print(",");
  Serial.println(fsrLittleRight); //coordinate[13] button9
  //Serial.print(fsrLittleRight); //coordinate[13] button9

  displayCalStatus();
  
  unsigned long currentMillis = millis();
  if (Serial.available() > 0){
    
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read(); 
    if (incomingByte == 'G') {
      setColor(0, 255, 0);  // green
    }
    else if (incomingByte == 'B') {
      setColor(0, 0, 255);  // blue
    }
    
    // activate left vibration motor
    if (incomingByte == '1' && motorState1 == LOW ) {
      previousMillis = currentMillis;
      motorState1 = HIGH;
    }
    // activate right vibration motor
    else if (incomingByte == '2' && motorState2 == LOW){
      previousMillis = currentMillis;
      motorState2 = HIGH;
    }
  }
  
  // deactivate left vibration motor after interval
  if ( motorState1 == HIGH && currentMillis - previousMillis >= interval) {
    motorState1 = LOW;
  }
  // deactivate right vibration motor after interval
  else if ( motorState2 == HIGH && currentMillis - previousMillis >= interval){
    motorState2 = LOW;
  }
  
  // trigger action on vibration motors
  digitalWrite(vibMotor1, motorState1);
  digitalWrite(vibMotor2, motorState2);
}


void setColor(int red, int green, int blue)
{
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);  
}


void displayCalStatus(void)
{
  /* Get the four calibration values (0..3) */
  /* Any sensor data reporting 0 should be ignored, */
  /* 3 means 'fully calibrated" */
  uint8_t system, gyro, accel, mag;
  system = gyro = accel = mag = 0;
  bno.getCalibration(&system, &gyro, &accel, &mag);

  // set color turquoise if any sensor calibration is below 3
  if (gyro < 3 || accel < 3 || mag < 3){
    setColor(0, 255, 255);
    if (system < 3){
      setColor(255, 255, 0);
    }
  }
  else{
    setColor(0, 255, 0);
  }
  // set color red if system is < 3
  //if (system < 3){
  //  setColor(255, 0, 0);
  //}

//  /* The data should be ignored until the system calibration is > 0 */
//  Serial.print("\t");
//  if (!system)
//  {
//    Serial.print("! ");
//  }

  /* Display the individual values */
//  Serial.print("Sys:");
//  Serial.print(system, DEC);
//  Serial.print(",");
//  Serial.print(gyro, DEC);
//  Serial.print(",");
//  Serial.print(accel, DEC);
//  Serial.print(",");
//  Serial.println(mag, DEC);
}
