// I2C device class (I2Cdev) demonstration Arduino sketch for MPU6050 class using DMP (MotionApps v2.0)
// 6/21/2012 by Jeff Rowberg <jeff@rowberg.net>
// Updates should (hopefully) always be available at https://github.com/jrowberg/i2cdevlib

/* ============================================
I2Cdev device library code is placed under the MIT license
Copyright (c) 2012 Jeff Rowberg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
===============================================
*/

// I2Cdev and MPU6050 must be installed as libraries, or else the .cpp/.h files
// for both classes must be in the include path of your project
#include "I2Cdev.h"

#include "MPU6050_6Axis_MotionApps20.h"

// Arduino Wire library is required if I2Cdev I2CDEV_ARDUINO_WIRE implementation
// is used in I2Cdev.h
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

// class default I2C address is 0x68
// specific I2C addresses may be passed as a parameter here
// AD0 low = 0x68 (default for SparkFun breakout and InvenSense evaluation board)
// AD0 high = 0x69
MPU6050 mpu;
//MPU6050 mpu(0x69); // <-- use for AD0 high

/* =========================================================================
   NOTE: In addition to connection 3.3v, GND, SDA, and SCL, this sketch
   depends on the MPU-6050's INT pin being connected to the Arduino's
   external interrupt #0 pin. On the Arduino Uno and Mega 2560, this is
   digital I/O pin 2.
 * ========================================================================= */

/* =========================================================================
   NOTE: Arduino v1.0.1 with the Leonardo board generates a compile error
   when using Serial.write(buf, len). The Teapot output uses this method.
   The solution requires a modification to the Arduino USBAPI.h file, which
   is fortunately simple, but annoying. This will be fixed in the next IDE
   release. For more info, see these links:

   http://arduino.cc/forum/index.php/topic,109987.0.html
   http://code.google.com/p/arduino/issues/detail?id=958
 * ========================================================================= */

#define OUTPUT_READABLE_YAWPITCHROLL

#define INTERRUPT_PIN 2  // use pin 2 on Arduino Uno & most boards
bool blinkState = false;

// MPU control/status vars
bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer

// orientation/motion vars
Quaternion q;           // [w, x, y, z]         quaternion container
VectorInt16 aa;         // [x, y, z]            accel sensor measurements
VectorInt16 aaReal;     // [x, y, z]            gravity-free accel sensor measurements
VectorInt16 aaWorld;    // [x, y, z]            world-frame accel sensor measurements
VectorFloat gravity;    // [x, y, z]            gravity vector
float euler[3];         // [psi, theta, phi]    Euler angle container
float ypr[3];           // [yaw, pitch, roll]   yaw/pitch/roll container and gravity vector

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

uint32_t timer;
int incomingByte;

// The pin numbers for the RGB LED
int redPin = 6;
int greenPin = 5;
int bluePin = 4;

const int vibMotor1 = 13;
int vibMotor2 = 12;
int motorState1 = LOW;
int motorState2 = LOW;

unsigned long previousMillis = 0; // will store last time the motor state was updated
const long interval = 100; // number of millisecs that Motor's are on - all two motors use this


// ================================================================
// ===               INTERRUPT DETECTION ROUTINE                ===
// ================================================================

volatile bool mpuInterrupt = false;     // indicates whether MPU interrupt pin has gone high
void dmpDataReady() {
    mpuInterrupt = true;
}

// ================================================================
// ===                      INITIAL SETUP                       ===
// ================================================================

void setup() {
    // join I2C bus (I2Cdev library doesn't do this automatically)
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
        Wire.setClock(400000); // 400kHz I2C clock. Comment this line if having compilation difficulties
    #elif I2CDEV_IMPLEMENTATIJON == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

    // initialize serial communication
    Serial.begin(115200);
    while (!Serial); // wait for Leonardo enumeration, others continue immediately

    // initialize device
    //Serial.println(F("Initializing I2C devices..."));
    mpu.initialize();
    pinMode(INTERRUPT_PIN, INPUT);

    // verify connection
    //Serial.println(F("Testing device connections..."));
    //Serial.println(mpu.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));

    // wait for ready
    //Serial.println(F("\nSend any character to begin DMP programming and demo: "));
    //while (Serial.available() && Serial.read()); // empty buffer
    //while (!Serial.available());                 // wait for data
    //while (Serial.available() && Serial.read()); // empty buffer again

    // load and configure the DMP
    //Serial.println(F("Initializing DMP..."));
    devStatus = mpu.dmpInitialize();

    // supply your own gyro offsets here, scaled for min sensitivity
//    // Old MPU
//    mpu.setXGyroOffset(84);
//    mpu.setYGyroOffset(-30);
//    mpu.setZGyroOffset(-15);
//    mpu.setZAccelOffset(1276);
//    // Old MPU 2.0
//    mpu.setXGyroOffset(87);
//    mpu.setYGyroOffset(-31);
//    mpu.setZGyroOffset(20);
//    mpu.setZAccelOffset(-3158);
//    mpu.setZAccelOffset(-1401);
//    mpu.setZAccelOffset(1239);// x,y-3158,   -1401
    // Old MPU 2.0
    mpu.setXGyroOffset(86);
    mpu.setYGyroOffset(-29);
    mpu.setZGyroOffset(12);
    mpu.setZAccelOffset(-3167);
    mpu.setZAccelOffset(-1403);
    mpu.setZAccelOffset(1239);// x,y-3158,   -1401
//    // New MPU
//    mpu.setXGyroOffset(45);
//    mpu.setYGyroOffset(-24);
//    mpu.setZGyroOffset(-22);
//    //mpu.setXAccelOffset(-3748);
//    mpu.setYAccelOffset(-1107);
//    //mpu.setZAccelOffset(3106);

    // make sure it worked (returns 0 if so)
    if (devStatus == 0) {
        // Calibration Time: generate offsets and calibrate our MPU6050
        mpu.CalibrateAccel(6);
        mpu.CalibrateGyro(6);
        //mpu.PrintActiveOffsets();
        // turn on the DMP, now that it's ready
        //Serial.println(F("Enabling DMP..."));
        mpu.setDMPEnabled(true);

        //enable Arduino interrupt detection
        //Serial.print(F("Enabling interrupt detection (Arduino external interrupt "));
        //Serial.print(digitalPinToInterrupt(INTERRUPT_PIN));
        //Serial.println(F(")..."));
        attachInterrupt(digitalPinToInterrupt(INTERRUPT_PIN), dmpDataReady, RISING);
        mpuIntStatus = mpu.getIntStatus();

        // set our DMP Ready flag so the main loop() function knows it's okay to use it
        //Serial.println(F("DMP ready! Waiting for first interrupt..."));
        dmpReady = true;

        // get expected DMP packet size for later comparison
        packetSize = mpu.dmpGetFIFOPacketSize();
    } else {
        // ERROR!
        // 1 = initial memory load failed
        // 2 = DMP configuration updates failed
        // (if it's going to break, usually the code will be 1)
        //Serial.print(F("DMP Initialization failed (code "));
        //Serial.print(devStatus);
        //Serial.println(F(")"));
    }

    // configure LED and Vibration Motor Pins as output
    pinMode(redPin, OUTPUT);
    pinMode(greenPin, OUTPUT);
    pinMode(bluePin, OUTPUT); 
    pinMode(vibMotor1, OUTPUT);
    pinMode(vibMotor2, OUTPUT);

    timer = micros();

    setColor(0, 0, 255);
}

// ================================================================
// ===                    MAIN PROGRAM LOOP                     ===
// ================================================================

void loop() {
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

  timer = micros();

  
    // if programming failed, don't try to do anything
    if (!dmpReady) return;

    // wait for MPU interrupt or extra packet(s) available
    while (!mpuInterrupt && fifoCount < packetSize) {
        if (mpuInterrupt && fifoCount < packetSize) {
          // try to get out of the infinite loop 
          fifoCount = mpu.getFIFOCount();
        }  
        // other program behavior stuff here
        // if you are really paranoid you can frequently test in between other
        // stuff to see if mpuInterrupt is true, and if so, "break;" from the
        // while() loop to immediately process the MPU data
    }

    // reset interrupt flag and get INT_STATUS byte
    mpuInterrupt = false;
    mpuIntStatus = mpu.getIntStatus();

    // get current FIFO count
    fifoCount = mpu.getFIFOCount();
	if(fifoCount < packetSize){
	        //Lets go back and wait for another interrupt. We shouldn't be here, we got an interrupt from another event
			// This is blocking so don't do it   while (fifoCount < packetSize) fifoCount = mpu.getFIFOCount();
	}
    // check for overflow (this should never happen unless our code is too inefficient)
    else if ((mpuIntStatus & _BV(MPU6050_INTERRUPT_FIFO_OFLOW_BIT)) || fifoCount >= 1024) {
        // reset so we can continue cleanly
        mpu.resetFIFO();
      //  fifoCount = mpu.getFIFOCount();  // will be zero after reset no need to ask
        Serial.println(F("FIFO overflow!"));

    // otherwise, check for DMP data ready interrupt (this should happen frequently)
    } else if (mpuIntStatus & _BV(MPU6050_INTERRUPT_DMP_INT_BIT)) {

        // read a packet from FIFO
	while(fifoCount >= packetSize){ // Lets catch up to NOW, someone is using the dreaded delay()!
		mpu.getFIFOBytes(fifoBuffer, packetSize);
		// track FIFO count here in case there is > 1 packet available
		// (this lets us immediately read more without waiting for an interrupt)
		fifoCount -= packetSize;
	}

        #ifdef OUTPUT_READABLE_YAWPITCHROLL
            // display Euler angles in degrees
            mpu.dmpGetQuaternion(&q, fifoBuffer);
            mpu.dmpGetGravity(&gravity, &q);
            mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
            
            yaw = (ypr[0] * 180/M_PI);
            roll = (ypr[1] * 180/M_PI);
            pitch = (ypr[2] * 180/M_PI);
            /**
            yaw_pre = yaw_filtered;
            yaw_filtered = yaw_pre + 0.5 * (yaw - yaw_pre);
            if(abs(oldDataYaw - yaw_filtered) <= 0.03){
              yaw_filtered = oldDataYaw;
            }
            oldDataYaw = yaw_filtered;
*/
            yaw_pre = yaw_filtered;
            yaw_filtered = 0.2 * yaw + 0.8 * yaw_pre;
            if(abs(oldDataYaw - yaw_filtered) <= 0.04){
              yaw_filtered = oldDataYaw;
            }
            oldDataYaw = yaw_filtered;

            pitch_pre = pitch_filtered;
            pitch_filtered = 0.2 * pitch + 0.8 * pitch_pre;
            if(abs(oldDataPitch - pitch_filtered) <= 0.04){
              pitch_filtered = oldDataPitch;
            }
            oldDataPitch = pitch_filtered;

            roll_pre = roll_filtered;
            roll_filtered = 0.2 * roll + 0.8 * roll_pre;
            if(abs(oldDataRoll - roll_filtered) <= 0.04){
              roll_filtered = oldDataRoll;
            }
            oldDataRoll = roll_filtered;
            
           
            //Serial.print(timer); // For graphic generation
            //Serial.print(",");     

            // Old MPU
            Serial.print(yaw_filtered); //coordinate[0]
            Serial.print(",");
            //Serial.print(yaw);
            //Serial.print(",");
            Serial.print(pitch_filtered); //coordinate[1]
            Serial.print(",");
            //Serial.print(pitch);
            //Serial.print(",");
            Serial.print(roll_filtered); //coordinate[14] for scrolling
            Serial.print(",");

//            // New MPU
//            Serial.print(pitch_filtered); //coordinate[0]
//            Serial.print(",");
//            //Serial.print(yaw);
//            //Serial.print(",");
//            Serial.print(yaw_filtered); //coordinate[1]
//            Serial.print(",");
//            //Serial.print(pitch);
//            //Serial.print(",");
//            Serial.print(roll_filtered); //coordinate[14] for scrolling
//            Serial.print(",");
            
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
            //Serial.print(",");
            
            
            
            
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
        #endif
}

void setColor(int red, int green, int blue)
{
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);  
}
