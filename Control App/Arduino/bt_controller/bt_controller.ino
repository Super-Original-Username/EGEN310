#include <arduino.h>
#include <SoftwareSerial.h>

SoftwareSerial BT(2,3);
int motors_left = 11;
int motors_right = 12;
int BT_in = [0,0,0]; //[speed,turn_direction,turn_intensity]
bool start = false;

void setup{
    Serial.begin(9600);
    pinMode(motors_left, OUTPUT);
    pinMode(motors_right, OUTPUT);
}

void loop{
    while(start){
        if(!BT.available()){
            delay(5000); // Stops the vehicle for 5 seconds if the bluetooth connection is lost
        }
        BT_in = BT.read();
        // There are a few options here. I can either try to remember how the code from the EELE 101 cars worked, or I can try to get clever with 
        // scheduling and do some weird sort of threading
        
    }
}

void forward(){
    //spins the right motor cw and left motor ccw for a period of time
}

void backward(){
    //spins the right motor ccw and the left motor cw
}

void t_right(){
    //seems like we are doing tracks, so this will spin both motors ccw, for a TBD period of time
}

void t_left(){
    //spins both motors cw for a TBD period of time
}