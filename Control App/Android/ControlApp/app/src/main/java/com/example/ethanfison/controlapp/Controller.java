package com.example.ethanfison.controlapp;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothProfile;
import android.content.Context;
import android.support.annotation.NonNull;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Toast;
import android.support.v7.widget.Toolbar;

import me.aflak.bluetooth.Bluetooth;
import me.aflak.bluetooth.BluetoothCallback;

public class Controller extends AppCompatActivity {
    Context context = getApplicationContext();

    private DrawerLayout drawerLayout;

    @Override
    protected void onCreate(Bundle savedInstanceState){
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_controller);

        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        ActionBar actionBar = getSupportActionBar();
        actionBar.setDisplayHomeAsUpEnabled(true);
        actionBar.setHomeAsUpIndicator(R.drawable.ic_menu);

        drawerLayout = findViewById(R.id.drawer_layout);

        NavigationView navigationView = findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(
                new NavigationView.OnNavigationItemSelectedListener() {
                    @Override
                    public boolean onNavigationItemSelected(@NonNull MenuItem menuItem) {
                        menuItem.setChecked(true);
                        drawerLayout.closeDrawers();
                        return true;
                    }
                }
        );
    }

    @Override
    public boolean onOptionsItemsSelected(MenuItem item){
        switch (item.getItemId()){
            case android.R.id.home:
            drawerLayout.openDrawer(GravityCompat.START);
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

   /* Bluetooth BTA = new Bluetooth(context); //Initialization of bluetooth object using the android bluetooth library found on GitHub

    @Override
    protected void onStart(){
        super.onStart();
        BTA.onStart();
        BTA.enable();
    }

    @Override
    protected void onStop(){
        super.onStop();
        BTA.onStop();
    }

    BTA.setBluetoothCallback(new BluetoothCallback(){
        @Override
        public void onBluetoothTurningOn() {}

        @Override
        public void onBluetoothOn() {}

        @Override
        public void onBluetoothTurningOff() {}

        @Override
        public void onBluetoothOff() {}

        @Override
        public void onUserDeniedActivation() {
            // when using bluetooth.showEnableDialog()
            // you will also have to call bluetooth.onActivityResult()
        }
    });
    *//*if(BTA == null){
        CharSequence text = "Bluetooth not supported by this device";
        Toast.makeText(context, "Bluetooth not supported by this device", Toast.LENGTH_SHORT).show();
    }*//*

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_controller);
    }*/
}
