/*Author: Minh Nguyen
CS 496: Front end for Android/JAVA final project
*/

package com.example.minh.final496;

import android.app.AlertDialog;
import android.content.Intent;
import android.media.MediaPlayer;
import android.os.AsyncTask;
import android.support.v7.app.ActionBarActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
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


public class MainActivity extends ActionBarActivity {
    EditText usernameUPET;
    EditText passwordUPET;
    EditText confirmpwET;
    EditText usernameET;
    EditText passwordET;

    String getUser;
    String getPassword;
    String username;
    String password;
    String usernameUP;
    String passwordUP;
    String confirmpw;

    Button iBsignup;
    Button iBlogin;

    MediaPlayer successClick;
    MediaPlayer failClick;

    public static final String SERVER_URL = "http://final496minh.appspot.com/user";
    public static final String QUERY_URL = "http://final496minh.appspot.com/user/";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        successClick = MediaPlayer.create(this, R.raw.button_click);
        failClick = MediaPlayer.create(this, R.raw.button_fail);

        usernameUPET = (EditText) findViewById(R.id.usernameUPET);
        passwordUPET = (EditText) findViewById(R.id.passwordUPET);
        confirmpwET = (EditText) findViewById(R.id.confirmpwET);
        iBsignup = (Button) findViewById(R.id.iBsignup);

        usernameET = (EditText) findViewById(R.id.usernameET);
        passwordET = (EditText) findViewById(R.id.passwordET);
        iBlogin = (Button) findViewById(R.id.iBlogin);

        iBlogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                username = usernameET.getText() + "";
                password = passwordET.getText() + "";

                if (username.length() == 0 || password.length() == 0){
                    failClick.start();
                    Toast.makeText(getApplicationContext(), "All fields must be filled",
                            Toast.LENGTH_LONG).show();
                    return;
                }
                LoginTask task = new LoginTask();
                task.execute();

            }
        });

        iBsignup.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                usernameUP = usernameUPET.getText() + "";
                passwordUP = passwordUPET.getText() + "";
                confirmpw = confirmpwET.getText() + "";

                if (usernameUP.length() == 0 || passwordUP.length() == 0){
                    failClick.start();
                    Toast.makeText(getApplicationContext(), "All fields must be filled",
                            Toast.LENGTH_LONG).show();
                    return;
                }

                if (!passwordUP.equals(confirmpw)){
                    failClick.start();
                    Toast.makeText(getApplicationContext(), "Password does not match",
                            Toast.LENGTH_LONG).show();
                    return;
                }
                successClick.start();
                SignUpTask task = new SignUpTask();
                task.execute();
            }
        });
    }

    private class LoginTask extends AsyncTask<String, String, String>{

        @Override
        protected String doInBackground(String... params) {
            HttpClient httpClient = new DefaultHttpClient();
            HttpGet request = new HttpGet(QUERY_URL + username);
            String result = null;


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
                getUser = jObj.getString("username");
                getPassword = jObj.getString("password");
            } catch (JSONException e) {
                e.printStackTrace();
            }

            return result;
        }

        protected void onPostExecute(String result){
            if (getUser.equals(username) && getPassword.equals(password)){
                successClick.start();
                Intent intent = new Intent(getApplicationContext(), DisplayInformation.class);
                intent.putExtra("username", username);
                startActivity(intent);
            }
            else {
                failClick.start();
                Toast.makeText(getApplicationContext(), "Incorrect login information",
                        Toast.LENGTH_LONG).show();
            }
        }

    }

    private class SignUpTask extends AsyncTask<String, String, String>{

        @Override
        protected String doInBackground(String... params) {
            String result = null;
            HttpClient httpClient = new DefaultHttpClient();
            HttpPost request = new HttpPost(SERVER_URL);
            List<NameValuePair> postParameters = new ArrayList<NameValuePair>();
            postParameters.add(new BasicNameValuePair("username",usernameUP));
            postParameters.add(new BasicNameValuePair("password", passwordUP));
            try {
                UrlEncodedFormEntity entity = new UrlEncodedFormEntity(postParameters);
                request.setEntity(entity);
                httpClient.execute(request);
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            } catch (ClientProtocolException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }

            return result;
        }

        protected void onPostExecute(String result){
            Toast.makeText(getApplicationContext(), "Account Successfuly Created",
                    Toast.LENGTH_LONG).show();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
