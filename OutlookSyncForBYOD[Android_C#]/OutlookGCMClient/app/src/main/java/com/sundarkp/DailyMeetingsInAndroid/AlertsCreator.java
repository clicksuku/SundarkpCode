package com.sundarkp.DailyMeetingsInAndroid;

import android.app.Activity;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.database.Cursor;
import android.net.Uri;
import android.provider.CalendarContract;
import android.util.Log;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.List;
import java.util.TimeZone;


/**
 * Created by sundarkp on 2/6/2015.
 */
public class AlertsCreator {

    public long Initialize(Activity activity)
    {
        try
        {
            long calendarId = getCalendarId(activity);

            if(-1 == calendarId) {
                createCustomCalendar(activity);
                calendarId = getCalendarId(activity);
            }
            return calendarId;
        }
        catch (Exception ex)
        {
            //Log.e("Error", ex.getMessage());
            return -1;
        }
    }

    public void CreateEvents(long calendarID, Activity activity,List<Appointment> appointmentList)
    {
        try {
            Calendar gregorian = new GregorianCalendar(TimeZone.getTimeZone("India"));
            SimpleDateFormat formatter = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");

            ContentResolver cr = activity.getContentResolver();
            ContentValues values = new ContentValues();


            for (Appointment appointment: appointmentList) {

                if(IsEventExisting(activity,appointment,calendarID))
                {
                    continue;
                }

                values.clear();
                values.put(CalendarContract.Events.CALENDAR_ID, calendarID);
                values.put(CalendarContract.Events.TITLE, appointment.Subject);
                values.put(CalendarContract.Events.ALL_DAY, 0);
                values.put(CalendarContract.Events.EVENT_TIMEZONE, "Asia/Calcutta");

                Date date = formatter.parse(appointment.Start);
                Long time = date.getTime();
                values.put(CalendarContract.Events.DTSTART, time);

                date = formatter.parse(appointment.End);
                time = date.getTime();
                values.put(CalendarContract.Events.DTEND, time);

                values.put(CalendarContract.Events.DESCRIPTION, appointment.Subject);
                values.put(CalendarContract.Events.EVENT_LOCATION, appointment.Location);
                values.put(CalendarContract.Events.ORGANIZER, appointment.Organizer);
                values.put(CalendarContract.Events.ACCESS_LEVEL, CalendarContract.Events.ACCESS_PRIVATE);
                values.put(CalendarContract.Events.HAS_ALARM, 1);

                Uri uri = cr.insert(CalendarContract.Events.CONTENT_URI, values);
                Long eventId = new Long(uri.getLastPathSegment());

                values.clear();
                values.put(CalendarContract.Reminders.EVENT_ID, eventId);
                values.put(CalendarContract.Reminders.METHOD, CalendarContract.Reminders.METHOD_ALERT);
                values.put(CalendarContract.Reminders.MINUTES, appointment.Reminder);
                cr.insert(CalendarContract.Reminders.CONTENT_URI, values);
            }
        }
        catch(Exception ex)
        {
            //Log.e("CreateCalendar", ex.getMessage());
        }

    }

    private long getCalendarId(Activity activity)
    {
        try
        {
            ContentResolver cr = activity.getContentResolver();
            String[] projection = new String[]{CalendarContract.Calendars._ID};

            Uri uri = CalendarContract.Calendars.CONTENT_URI;
            String selection = "((" + CalendarContract.Calendars.NAME + " = ?) AND ("
                    + CalendarContract.Calendars.ACCOUNT_NAME + " = ?) AND ("
                    + CalendarContract.Calendars.ACCOUNT_TYPE + " = ?) AND ("
                    + CalendarContract.Calendars.OWNER_ACCOUNT + " = ?))";

            String[] selectionArgs = new String[] {"SymcOutlook Custom Calendar","com.symcOutlook", CalendarContract.ACCOUNT_TYPE_LOCAL,
                    "sundarakumar_padmana@symantec.com"};

            Cursor cursor = cr.query(
                    uri,
                    projection,
                    selection,
                    selectionArgs,
                    null);

            if(cursor.moveToFirst()) {
                return cursor.getLong(0);
            }

            return -1;
        }
        catch(Exception ex)
        {
            return -1;
        }

    }


    private boolean IsEventExisting(Activity activity, Appointment appointment, Long calendarID)
    {
        try
        {
            ContentResolver cr = activity.getContentResolver();
            SimpleDateFormat formatter = new SimpleDateFormat("dd-MM-yyyy HH:mm:ss");
            String[] projection = new String[]{CalendarContract.Events._ID};

            Uri uri = CalendarContract.Events.CONTENT_URI;
            String selection = "((" + CalendarContract.Events.CALENDAR_ID + " = ?) AND ("
                    + CalendarContract.Events.TITLE + " = ?) AND ("
                    + CalendarContract.Events.DTSTART + " = ?) AND ("
                    + CalendarContract.Events.DTEND + " = ?) AND ("
                    + CalendarContract.Events.DESCRIPTION + " = ?) AND ("
                    + CalendarContract.Events.EVENT_LOCATION + " = ?) AND ("
                    + CalendarContract.Events.ORGANIZER + " = ?))";

            Date date = formatter.parse(appointment.Start);
            Long starttime = date.getTime();

            date = formatter.parse(appointment.End);
            Long endtime = date.getTime();


            String[] selectionArgs = new String[] {calendarID.toString(),appointment.Subject,
                    starttime.toString(), endtime.toString(),appointment.Subject, appointment.Location,
                    appointment.Organizer};

            Cursor cursor = cr.query(
                    uri,
                    projection,
                    selection,
                    selectionArgs,
                    null);

            if(cursor.moveToFirst()) {
                return true;
            }


            return false;
        }
        catch(Exception ex)
        {
            return false;
        }

    }



    private void createCustomCalendar(Activity activity)
    {
        try {
            ContentValues values = new ContentValues();
            values.put(
                    CalendarContract.Calendars.ACCOUNT_NAME,
                    "com.symcOutlook");
            values.put(
                    CalendarContract.Calendars.ACCOUNT_TYPE,
                    CalendarContract.ACCOUNT_TYPE_LOCAL);
            values.put(
                    CalendarContract.Calendars.NAME,
                    "SymcOutlook Custom Calendar");
            values.put(
                    CalendarContract.Calendars.CALENDAR_DISPLAY_NAME,
                    "SymcOutlook Custom Calendar");
            values.put(
                    CalendarContract.Calendars.CALENDAR_COLOR,
                    0xFF4FC8F0);
            values.put(
                    CalendarContract.Calendars.CALENDAR_ACCESS_LEVEL,
                    CalendarContract.Calendars.CAL_ACCESS_OWNER);
            values.put(
                    CalendarContract.Calendars.OWNER_ACCOUNT,
                    "sundarakumar_padmana@symantec.com");
            values.put(
                    CalendarContract.Calendars.CALENDAR_TIME_ZONE,
                    "Asia/Calcutta");
            values.put(
                    CalendarContract.Calendars.SYNC_EVENTS,
                    0);

            Uri.Builder builder =
                    CalendarContract.Calendars.CONTENT_URI.buildUpon();
            builder.appendQueryParameter(
                    CalendarContract.Calendars.ACCOUNT_NAME,
                    "com.symcOutlook");
            builder.appendQueryParameter(
                    CalendarContract.Calendars.ACCOUNT_TYPE,
                    CalendarContract.ACCOUNT_TYPE_LOCAL);
            builder.appendQueryParameter(
                    CalendarContract.CALLER_IS_SYNCADAPTER,
                    "true");
            Uri uri =
                    activity.getContentResolver().insert(builder.build(), values);
        }
        catch(Exception ex)
        {
            //Log.e("CreateCalendar", ex.getMessage());
        }
    }



}
