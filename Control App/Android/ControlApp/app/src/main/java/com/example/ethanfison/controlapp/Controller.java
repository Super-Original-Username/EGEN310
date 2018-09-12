package com.example.ethanfison.controlapp;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothProfile;
import android.content.Context;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Toast;

public class Controller extends AppCompatActivity {
    Context context = getApplicationContext();
    BluetoothAdapter BTA = BluetoothAdapter.getDefaultAdapter();

    private BluetoothProfile.ServiceListener BTProfileListener = new BluetoothProfile.ServiceListener() {
        @Override
        public void onServiceConnected(int i, BluetoothProfile bluetoothProfile) {

        }

        @Override
        public void onServiceDisconnected(int i) {

        }
    }
    if(BTA == null){
        CharSequence text = "Bluetooth not supported by this device";
        Toast.makeText(context, "Bluetooth not supported by this device", Toast.LENGTH_SHORT).show();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_controller);
    }
}
