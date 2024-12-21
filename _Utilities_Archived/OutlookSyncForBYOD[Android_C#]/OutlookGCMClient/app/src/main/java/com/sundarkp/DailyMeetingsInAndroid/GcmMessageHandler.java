package com.sundarkp.DailyMeetingsInAndroid;

import com.google.android.gms.gcm.GoogleCloudMessaging;
import android.app.IntentService;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.widget.Toast;


/**
 * An {@link IntentService} subclass for handling asynchronous task requests in
 * a service on a separate handler thread.
 * <p/>
 * TODO: Customize class - update intent actions and extra parameters.
 */
public class GcmMessageHandler extends IntentService {

    String response;
    private Handler handler;
    private EncryptionUtility encryptor;

    public GcmMessageHandler() {
        super("GcmMessageHandler");
        encryptor = new EncryptionUtility();
    }

    @Override
    public void onCreate() {
        super.onCreate();
        handler = new Handler();
    }


    @Override
    protected void onHandleIntent(Intent intent) {
        Bundle extras = intent.getExtras();

        GoogleCloudMessaging gcm = GoogleCloudMessaging.getInstance(this);
        String messageType = gcm.getMessageType(intent);

        response = extras.getString("meetings");

        try {
            String decryptedData = encryptor.decrypt(response,"TheDataIsEncrypted");

            Intent dialogIntent = new Intent(getBaseContext(), MeetingsActivity.class);
            dialogIntent.addFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT | Intent.FLAG_ACTIVITY_CLEAR_TASK | Intent.FLAG_ACTIVITY_NEW_TASK);
            Bundle b = new Bundle();
            b.putString("meetings", decryptedData);
            dialogIntent.putExtras(b);

            getApplication().startActivity(dialogIntent);
            GcmBroadcastReceiver.completeWakefulIntent(intent);
        }
        catch (Exception ex)
        {
            //Log.e("Error", ex.getMessage());
            return;
        }
    }

     public void showToast() {
         handler.post(new Runnable() {
             public void run() {
                 Toast.makeText(getApplicationContext(), response, Toast.LENGTH_LONG).show();
             }
         });

     }

}
