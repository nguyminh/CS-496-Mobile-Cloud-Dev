/*Author: Minh Nguyen
CS 496: Front end for Android/JAVA final project
*/

package com.example.minh.final496;

import android.content.Intent;
import android.media.MediaPlayer;
import android.os.AsyncTask;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpDelete;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;


public class DisplayInformation extends ActionBarActivity {

    TextView usernameTV;
    String username;
    Button iBlogout;

    EditText addclassET;
    Button iBaddclass;
    String addclass;

    TextView classTV;
    Button iBgetclass;
    String displayclass;

    EditText deleteclassET;
    Button iBdeleteclass;
    String deleteclass;

    MediaPlayer successClick;
    MediaPlayer failClick;

    public static final String ADDCLASS_URL = "http://final496minh.appspot.com/user";
    public static final String DELETECLASS_URL = "http://final496minh.appspot.com/user/";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_display_information);
        Intent intent = getIntent();
        username = intent.getStringExtra("username");
        iBlogout = (Button) findViewById(R.id.iBlogout);
        usernameTV = (TextView) findViewById(R.id.usernameTV);
        usernameTV.setText(username);

        addclassET = (EditText) findViewById(R.id.addclassET);
        iBaddclass = (Button) findViewById(R.id.iBaddclass);

        classTV = (TextView) findViewById(R.id.classTV);
        iBgetclass = (Button) findViewById(R.id.iBgetclass);

        deleteclassET = (EditText)findViewById(R.id.deleteclassET);
        iBdeleteclass = (Button)findViewById(R.id.iBdeleteclass);

        successClick = MediaPlayer.create(this, R.raw.button_click);
        failClick = MediaPlayer.create(this, R.raw.button_fail);

        iBlogout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                successClick.start();
                finish();
            }
        });

        iBdeleteclass.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                deleteclass = deleteclassET.getText() + "";
                if (deleteclass.length() == 0){
                    failClick.start();
                    Toast.makeText(getApplicationContext(), "Field is empty",
                            Toast.LENGTH_LONG).show();
                }
                successClick.start();
                deleteClassTask task = new deleteClassTask();
                task.execute();
            }
        });

        iBaddclass.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                addclass = addclassET.getText() + "";
                if (addclassET.length() == 0){
                    failClick.start();
                    Toast.makeText(getApplicationContext(), "Field is empty",
                            Toast.LENGTH_LONG).show();
                }
                successClick.start();
                addClassTask task = new addClassTask();
                task.execute();

            }
        });

        iBgetclass.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                successClick.start();
                getClassTask task = new getClassTask();
                task.execute();
            }
        });

    }

    private class deleteClassTask extends AsyncTask<String, String, String>{

        @Override
        protected String doInBackground(String... params) {
            String result = null;
            HttpClient httpClient = new DefaultHttpClient();
            HttpDelete request = new HttpDelete(DELETECLASS_URL + username + "/" + deleteclass);

            try {
                httpClient.execute(request);
            } catch (IOException e) {
                e.printStackTrace();
            }

            return result;
        }

        protected void onPostExecute(String result){
            Toast.makeText(getApplicationContext(), "Class Deleted!",
             Toast.LENGTH_LONG).show();
        }
    }


    private class getClassTask extends AsyncTask<String, String, String>{

        @Override
        protected String doInBackground(String... params) {
            String result = null;
            HttpClient httpClient = new DefaultHttpClient();
            HttpGet request = new HttpGet(ADDCLASS_URL + "/" + username);

            BufferedReader bufferedReader = null;
            StringBuffer stringBuffer = new StringBuffer("");
            try{
                HttpResponse response = httpClient.execute(request);

                bufferedReader = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));

                String line = "";
                String LineSeparator = System.getProperty(("line.separator"));

                while((line = bufferedReader.readLine()) != null){
                    stringBuffer.append(line + LineSeparator);
                }
                result = stringBuffer.toString();
                bufferedReader.close();

            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            } catch (ClientProtocolException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
            try {
                JSONArray jo = new JSONArray(result);
                JSONObject jObj = jo.getJSONObject(0);
                displayclass = jObj.getString("class_teach");

            } catch (JSONException e) {
                e.printStackTrace();
            }

            return result;
        }

        protected void onPostExecute(String result){
            TextView classTV = (TextView) findViewById(R.id.classTV);
            classTV.setText(displayclass);
        }
    }


    private class addClassTask extends AsyncTask<String, String, String> {

        @Override
        protected String doInBackground(String... params) {
            String result = null;
            HttpClient httpClient = new DefaultHttpClient();
            HttpPut request = new HttpPut(ADDCLASS_URL + "/" + username + "/" + addclass);
            try {
                httpClient.execute(request);
            } catch (IOException e) {
                e.printStackTrace();
            }

            return result;
        }

        protected void onPostExecute(String result){
            Toast.makeText(getApplicationContext(), "Class Successfully added",
                    Toast.LENGTH_LONG).show();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_display_information, menu);
        return true;
    }


}
