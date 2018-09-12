#include <arduino.h>

SoftwareSerial BT()
int motors_left = 11;
int motors_right = 12;
char BT_in = 0;
bool start = false;

void setup{
    Serial.begin(9600);
    pinMode(motors_left, OUTPUT);
    pinMode(motors_right, OUTPUT);
}

void loop{
    while(start){
        
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