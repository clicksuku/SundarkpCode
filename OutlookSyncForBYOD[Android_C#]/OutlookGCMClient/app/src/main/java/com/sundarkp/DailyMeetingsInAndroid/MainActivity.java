package com.sundarkp.DailyMeetingsInAndroid;


import android.annotation.TargetApi;
import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.AsyncTask;

import com.google.android.gms.gcm.GoogleCloudMessaging;

import android.view.Menu;
import android.view.MenuItem;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.io.IOException;

import android.view.GestureDetector;
import android.view.GestureDetector.OnGestureListener;
import android.view.MotionEvent;



public class MainActivity extends Activity implements  OnClickListener, OnGestureListener
{
    Button btnRegId;
    EditText etRegId;
    Button btnProjId;
    EditText etProjId;
    Button btnPack;

    GoogleCloudMessaging gcm;
    String regid;
    String PROJECT_NUMBER = "";

    private GestureDetector gDetector;
    private PreferencesHelper prefs;
    private static final String REGIDSET = "ISREGIDSET";

    float x1,x2;
    float y1, y2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        setupUI(findViewById(R.id.parentLayout));

        gDetector = new GestureDetector(this);
        prefs = new PreferencesHelper(getApplicationContext());

        btnRegId = (Button) findViewById(R.id.btnGetRegId);
        etRegId = (EditText) findViewById(R.id.etRegId);
        btnProjId = (Button) findViewById(R.id.btnProjectID);
        etProjId = (EditText) findViewById(R.id.etProjectId);

        btnPack = (Button) findViewById(R.id.btnPack);

        btnRegId.setOnClickListener(this);
        btnProjId.setOnClickListener(this);
        btnPack.setOnClickListener(this);
    }

    @TargetApi(Build.VERSION_CODES.CUPCAKE)
    public void getRegId(){
        new AsyncTask<Void, Void, String>() {
            @Override
            protected String doInBackground(Void... params) {
                String msg = "";
                try {
                    if (gcm == null) {
                        gcm = GoogleCloudMessaging.getInstance(getApplicationContext());
                    }
                    regid = gcm.register(PROJECT_NUMBER);
                    msg = regid;
                    //Log.i("GCM",  msg);

                } catch (IOException ex) {
                    msg = "Error :" + ex.getMessage();

                }
                return msg;
            }

            @Override
            protected void onPostExecute(String msg)
            {
                etRegId.setText(msg + "\n");
                prefs.SavePreferences(REGIDSET,true);
            }
        }.execute(null, null, null);
    }

    @Override
    public void onClick(View v) {
        if(v.getId() == btnProjId.getId())
        {
            String projIdVal = etProjId.getText().toString();
            if(projIdVal.length() == 0)
            {
                Toast.makeText(this, "Project ID is Empty!!", Toast.LENGTH_SHORT).show();
            }

            try
            {
                PROJECT_NUMBER = projIdVal;
                Toast.makeText(this, "ProjectID Set!", Toast.LENGTH_SHORT).show();
            }
            catch(NumberFormatException nfe)
            {
                System.out.println("Could not parse " + nfe);
                Toast.makeText(this, "Project ID is Invalid!!", Toast.LENGTH_SHORT).show();
            }

        }
        else if(v.getId() == btnRegId.getId()) {
            if(etProjId.length()!=0) {
                Toast.makeText(this, "RegID generated!", Toast.LENGTH_SHORT).show();
                getRegId();
            }
            else
            {
                Toast.makeText(this, "Set a Project ID!!", Toast.LENGTH_SHORT).show();
            }
        }
        else if(v.getId() == btnPack.getId()) {
            String regID = etRegId.getText().toString();

            if(regID.length()!=0) {
                Toast.makeText(this, "Mail RegID", Toast.LENGTH_SHORT).show();

                Intent send = new Intent(Intent.ACTION_SENDTO);
                String uriText = "mailto:" + Uri.encode("email@symantec.com") +
                        "?subject=" + Uri.encode("Device RegID") +
                        "&body=" + Uri.encode(regID);
                Uri uri = Uri.parse(uriText);

                send.setData(uri);
                startActivity(Intent.createChooser(send, "Sending mail..."));
            }
            else
            {
                Toast.makeText(this, "Click Generate first!!", Toast.LENGTH_SHORT).show();
            }
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
        /*if (id == R.id.action_settings) {
            return true;
        }*/

        return super.onOptionsItemSelected(item);
    }


    @Override
    public boolean onDown(MotionEvent arg0) {
        return false;
    }

    @Override
    public boolean onFling(MotionEvent start, MotionEvent finish, float xVelocity, float yVelocity) {
        return false;
    }
    @Override
    public void onLongPress(MotionEvent arg0) {
        return;
    }
    @Override
    public boolean onScroll(MotionEvent arg0, MotionEvent arg1, float arg2, float arg3) {
        return false;
    }
    @Override
    public void onShowPress(MotionEvent arg0) {
        // TODO Auto-generated method stub
    }
    @Override
    public boolean onSingleTapUp(MotionEvent arg0) {
        return false;
    }

    @Override
    public boolean onTouchEvent(MotionEvent touchevent) {
        //return gDetector.onTouchEvent(me);
        switch (touchevent.getAction())
        {
            // when user first touches the screen we get x and y coordinate
            case MotionEvent.ACTION_DOWN:
            {
                x1 = touchevent.getX();
                y1 = touchevent.getY();
                break;
            }
            case MotionEvent.ACTION_UP:
            {
                x2 = touchevent.getX();
                y2 = touchevent.getY();

                //if left to right sweep event on screen
                if (x1 < x2)
                {
                    //Toast.makeText(this, "Left to Right Swap Performed", Toast.LENGTH_LONG).show();
                    TransitionToLandingPage();
                }
                // if right to left sweep event on screen
                if ((x1 > x2) && (x1-x2 > 400))
                {
                    //Toast.makeText(this, "Right to Left Swap Performed", Toast.LENGTH_LONG).show();
                    TransitionToMeetingsList();
                }

                break;
            }
        }
        return false;
    }

    private void TransitionToMeetingsList()
    {
        try {
            Intent intent = new Intent(this, MeetingsActivity.class);
            intent.addFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT | Intent.FLAG_ACTIVITY_NEW_TASK);
            startActivity(intent);
            overridePendingTransition(R.anim.right_in, R.anim.left_out);
        }
        catch (Exception ex)
        {
            //Log.e("Error", ex.getMessage());
            return;
        }
    }

    private void TransitionToLandingPage()
    {
        try {
            Intent intent = new Intent(this, LandingPageActivity.class);
            intent.addFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT | Intent.FLAG_ACTIVITY_NEW_TASK);
            startActivity(intent);
            overridePendingTransition(R.anim.left_in, R.anim.right_out);
        }
        catch (Exception ex)
        {
            //Log.e("Error", ex.getMessage());
            return;
        }
    }

    private void setupUI(View view) {
        //Set up touch listener for non-text box views to hide keyboard.
        if(!(view instanceof EditText)) {
            view.setOnTouchListener(new View.OnTouchListener() {
                public boolean onTouch(View v, MotionEvent event) {
                    hideSoftKeyboard(MainActivity.this);
                    return false;
                }
            });
        }
        //If a layout container, iterate over children and seed recursion.
        if (view instanceof ViewGroup) {
            for (int i = 0; i < ((ViewGroup) view).getChildCount(); i++) {
                View innerView = ((ViewGroup) view).getChildAt(i);
                setupUI(innerView);
            }
        }
    }

    private static void hideSoftKeyboard(Activity activity) {
        InputMethodManager inputMethodManager = (InputMethodManager)  activity.getSystemService(Activity.INPUT_METHOD_SERVICE);
        inputMethodManager.hideSoftInputFromWindow(activity.getCurrentFocus().getWindowToken(), 0);
    }
}
