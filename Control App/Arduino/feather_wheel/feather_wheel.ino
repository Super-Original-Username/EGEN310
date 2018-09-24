#include <bluefruit.h>

BLEUart bleuart;

uint8_t readPacket(BLEUart *ble_uart, uint8_t timeout);
float parseFloat(uint8_t *buffer);

extern uint8_t packetbuffer[];

void setup()
{
    Serial.begin(115200);

    Bluefruit.begin();
    Bluefruit.setTxPower(4); // This sets the transmit power to the highest setting for the bluetooth module
    Bluefruit.setName("FeatherWheel");

    bleuart.begin(); // Launches the low-energy uart service

    startAdv(); // Begins advertising for the bluetooth module
}

void startAdv()
{
    Bluefruit.Advertising.addFlags(BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE);
    Bluefruit.Advertising.addTxPower();

    Bluefruit.Advertising.addService(bleuart);
    Bluefruit.ScanResponse.addName();

    Bluefruit.Advertising.restartOnDisconnect(true);
    Bluefruit.Advertising.setInterval(32, 244); // in unit of 0.625 ms
    Bluefruit.Advertising.setFastTimeout(30);   // number of seconds in fast mode
    Bluefruit.Advertising.start(0);             // 0 = Don't stop advertising after n seconds
}

void loop()
{
    if (packetbuffer[1] == 'B')
    {
        int lin_dir = 1;
        uint8_t speed = packetbuffer[2] - '0';
        boolean linear_speed = packetbuffer[3] - '0';
        int turn_speed = packetbuffer[4] - '0';
        boolean flip_controls = packetbuffer[5] - '0';
        boolean complete_stop = packetbuffer[6] - '0';
        Serial.print("Linear Speed: ");
        Serial.println(linear_speed * speed);
        if (flip_controls)
        {
            Serial.println("Standard controls");
        }
        else
        {
            Serial.println("Flipped controls");
        }
        if (complete_stop)
            Serial.println("Movement enabled") else Serial.println("Movement Disabled")
    }
}