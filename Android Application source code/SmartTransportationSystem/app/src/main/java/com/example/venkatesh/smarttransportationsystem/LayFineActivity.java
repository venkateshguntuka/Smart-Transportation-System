package com.example.venkatesh.smarttransportationsystem;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.firebase.client.ChildEventListener;
import com.firebase.client.Firebase;
import com.firebase.client.FirebaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.firebase.client.ValueEventListener;
import com.firebase.client.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import android.util.Log;

import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.lang.*;
import android.text.util.*;
import com.firebase.client.Query;


/**
 * Created by venkatesh on 23-03-2017.
 */
public class LayFineActivity extends Activity {

    private EditText sts_id, fine_amount;
    private Button fine_btn;

    Firebase ref;
    private DatabaseReference mDatabase;

    public void onCreate(Bundle b) {
        super.onCreate(b);
        setContentView(R.layout.activity_layfines);
        sts_id = (EditText) findViewById(R.id.editText);
        fine_amount = (EditText) findViewById(R.id.editText2);
        fine_btn = (Button) findViewById(R.id.layfine);


        mDatabase = FirebaseDatabase.getInstance().getReference().child("database");

        fine_btn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String stsID = sts_id.getText().toString();
                String fineAmount = fine_amount.getText().toString();
                onPost(stsID, fineAmount);
                sts_id.setText("");
                fine_amount.setText("");

            }
        });


    }


        public void onPost(String id, String fine)
        {
            mDatabase = FirebaseDatabase.getInstance().getReference().child("database").child(id).child("FINE").child("total_fine");
            mDatabase.setValue(fine);
            Toast.makeText(this, "Fine updated successfully!", Toast.LENGTH_LONG).show();
            
        }


    }



