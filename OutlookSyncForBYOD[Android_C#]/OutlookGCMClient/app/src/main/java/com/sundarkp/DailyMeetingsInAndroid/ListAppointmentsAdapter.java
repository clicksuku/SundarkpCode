package com.sundarkp.DailyMeetingsInAndroid;

import android.content.Context;
import android.provider.CalendarContract;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;

import java.util.List;

/**
 * Created by sundarkp on 05-02-2015.
 */
public class ListAppointmentsAdapter extends BaseAdapter
{
    Context _context;
    protected List<Appointment> _appointments;
    LayoutInflater _inflater;

    public ListAppointmentsAdapter(Context context, List<Appointment> appointments)
    {
        this._context = context;
        this._appointments = appointments;
        this._inflater = LayoutInflater.from(context);
    }

    public int getCount()
    {
        return _appointments.size();
    }

    public Appointment getItem(int position)
    {
        return _appointments.get(position);
    }

    public long getItemId(int position)
    {
        return position;
    }

    public View getView(int position, View convertView, ViewGroup parent)
    {
        ViewHolder holder;
        if(convertView==null)
        {
            holder = new ViewHolder();
            convertView = this._inflater.inflate(R.layout.listitem,parent,false);

            holder.txtOrganizer = (TextView) convertView.findViewById(R.id.etOrganizer);
            holder.txtSubject = (TextView) convertView.findViewById(R.id.etSubject);
            holder.txtLocation = (TextView) convertView.findViewById(R.id.etLocation);

            holder.txtStart = (TextView) convertView.findViewById(R.id.etStart);
            holder.txtEnd = (TextView) convertView.findViewById(R.id.etEnd);

            convertView.setTag(holder);
        }
        else
        {
            holder = (ViewHolder)convertView.getTag();
        }

        Appointment apt = (Appointment)_appointments.get(position);

        holder.txtOrganizer.setText(apt.Organizer);
        holder.txtSubject.setText(apt.Subject);
        holder.txtLocation.setText(apt.Location);
        holder.txtStart.setText(apt.Start);
        holder.txtEnd.setText(apt.End);

        return  convertView;
    }

    private class ViewHolder
    {
        TextView txtOrganizer;
        TextView txtLocation;
        TextView txtSubject;

        TextView txtStart;
        TextView txtEnd;
    }


}
