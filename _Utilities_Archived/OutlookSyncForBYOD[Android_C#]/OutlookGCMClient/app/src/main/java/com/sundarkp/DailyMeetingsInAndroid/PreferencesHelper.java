package com.sundarkp.DailyMeetingsInAndroid;


import android.content.Context;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;


/**
 * Created by sundarkp on 2/9/2015.
 */
public class PreferencesHelper {

    private SharedPreferences sharedPreferences;
    private Editor editor;
    public static final String MyPREFERENCES = "MyPrefs" ;

    public PreferencesHelper(Context context) {
        this.sharedPreferences = context.getSharedPreferences(MyPREFERENCES, Context.MODE_PRIVATE);
        this.editor = sharedPreferences.edit(); }


    public boolean GetPreferencesBoolean(String key) {
        return sharedPreferences.getBoolean(key,false);
    }

    public String GetPreferences(String key) {
        return sharedPreferences.getString(key, "");
    }

    public void SavePreferences(String key, String value) {
        editor.putString(key, value);
        editor.commit();
    }

    public void SavePreferences(String key, boolean value) {
        editor.putBoolean(key, value);
        editor.commit();
    }
}
