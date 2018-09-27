#include <string.h>
#include <Arduino.h>
#include <bluefruit.h>

#define PACKET_CONTROLS_LEN (20)

#define READ_BUFFERSIZE (20)

uint8_t packetbuffer[READ_BUFFERSIZE + 1];

float parseFloat(uint8_t *buffer){
    float f;
    memcpy(&f, buffer, 4);
    return f;
}

uint8_t readPacket(BLEUart *ble_uart, uint8_t timeout){
    uint16_t origtimeout = timeout, replyidx = 0;

  memset(packetbuffer, 0, READ_BUFFERSIZE);

  while (timeout--) {
    if (replyidx >= 20) break;

    while (ble_uart->available()) {
      char c =  ble_uart->read();
      if (c == '!') {
        replyidx = 0;
      }
      packetbuffer[replyidx] = c;
      replyidx++;
      timeout = origtimeout;
    }
    
    if (timeout == 0) break;
    delay(1);
  }

  packetbuffer[replyidx] = 0;  // null term

  if (!replyidx)  // no data or timeout 
    return 0;
  if (packetbuffer[0] != '!')  // doesn't start with '!' packet beginning
    return 0;
  
  // check checksum!
  uint8_t xsum = 0;
  uint8_t checksum = packetbuffer[replyidx-1];
  
  for (uint8_t i=0; i<replyidx-1; i++) {
    xsum += packetbuffer[i];
  }
  xsum = ~xsum;

  if (xsum != checksum) // Throws an error if the checksums don't match
  {
    Serial.println("Checksum mismatch");
    return 0;
  }
  
  // checksum passed!
  return replyidx;
}