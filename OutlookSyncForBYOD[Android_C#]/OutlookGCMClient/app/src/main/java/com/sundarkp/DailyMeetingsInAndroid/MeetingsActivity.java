package com.sundarkp.DailyMeetingsInAndroid;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.opengl.Visibility;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Debug;
import android.util.Log;

import android.view.Menu;
import android.view.MenuItem;

import android.widget.ListView;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;
import java.util.List;

import android.view.View;
import android.view.View.OnClickListener;
import java.io.IOException;

import android.view.GestureDetector;
import android.view.GestureDetector.OnGestureListener;
import android.view.MotionEvent;
import android.widget.TextView;
import android.widget.Toast;


public class MeetingsActivity extends Activity implements OnClickListener, OnGestureListener {

    float x1,x2;
    float y1, y2;

    TextView noMeetLabel;

    AlertsCreator _alertsCreator;
    long calendarId=-1;
    String meetings;

    private static final String MEETINGS = "meetingsKey";
    private PreferencesHelper prefs;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_meetings);

        noMeetLabel = (TextView) findViewById(R.id.meetingsLabel);

        _alertsCreator = new AlertsCreator();
        calendarId = _alertsCreator.Initialize(this);

        prefs = new PreferencesHelper(getApplicationContext());
        InitializeListView();
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        // getIntent() should always return the most recent
        setIntent(intent);
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_meetings, menu);
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
    public void onClick(View v) {
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
    public boolean dispatchTouchEvent(MotionEvent touchevent)
    {
        switch (touchevent.getAction()) {
            case MotionEvent.ACTION_DOWN: {
                x1 = touchevent.getX();
                y1 = touchevent.getY();
                break;
            }
            case MotionEvent.ACTION_UP: {
                x2 = touchevent.getX();
                y2 = touchevent.getY();
                if ((x1 < x2)&&(x2-x1 > 400)) {
                    //Toast.makeText(this, "Left to Right Swap Performed", Toast.LENGTH_LONG).show();
                    TransitionToMainActivity();
                }
                if (x1 > x2) {
                    //Toast.makeText(this, "Right to Left Swap Performed", Toast.LENGTH_LONG).show();
                    //TransitionToLandingPage();
                }
                break;
            }
        }
        return super.dispatchTouchEvent(touchevent);
    }

    private void TransitionToMainActivity()
    {
        try {
            Intent intent = new Intent(this, MainActivity.class);
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

    private void TransitionToLandingPage()
    {
        try {
            Intent intent = new Intent(this, LandingPageActivity.class);
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

    private void InitializeListView()
    {

        try {
            Bundle b = getIntent().getExtras();

            if (b != null)
            {
                meetings = b.getString("meetings");
                prefs.SavePreferences(MEETINGS,meetings);
                List<Appointment> appointments = ParseAppointments(meetings);

                noMeetLabel.setVisibility(View.INVISIBLE);
                Context context = this;
                ListView listMeeting = (ListView) findViewById(R.id.listMeetings);
                ListAppointmentsAdapter appointmentsAdapter = new ListAppointmentsAdapter(this, appointments);
                listMeeting.setAdapter(appointmentsAdapter);

                CreateReminders(appointments);
                return;
            }
            else
            {
                meetings = prefs.GetPreferences(MEETINGS);

                if ((meetings==null)||(meetings.length() == 0))
                {
                    noMeetLabel.setText("No Meetings Today!!");
                    noMeetLabel.setVisibility(View.VISIBLE);
                    return;
                }
                else
                {
                    noMeetLabel.setVisibility(View.INVISIBLE);
                    List<Appointment> appointments = ParseAppointments(meetings);

                    Context context = this;
                    ListView listMeeting = (ListView) findViewById(R.id.listMeetings);
                    ListAppointmentsAdapter appointmentsAdapter = new ListAppointmentsAdapter(this, appointments);
                    listMeeting.setAdapter(appointmentsAdapter);
                    return;
                }
            }
        }
        catch (Exception ex) {
            //Log.w("OutlookGCM", ex.getMessage());
        }
    }

    private List<Appointment> ParseAppointments(String data)
    {
        Gson gson = new Gson();
        Type collectionType = new TypeToken<List<Appointment>>() {}.getType();
        List<Appointment> meetings = gson.fromJson(data, collectionType);
        return meetings;
    }

    private void CreateReminders(List<Appointment> appointments)
    {
        _alertsCreator.CreateEvents(calendarId,this,appointments);
    }

}
