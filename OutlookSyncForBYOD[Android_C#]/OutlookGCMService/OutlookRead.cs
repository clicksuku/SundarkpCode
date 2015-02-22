using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using System.Reflection;
using System.Runtime.InteropServices;

using Outlook = Microsoft.Office.Interop.Outlook;
using Office = Microsoft.Office.Core;
using System.Web.Script.Serialization;

namespace OutlookGCMService
{
    internal class OutlookRead
    {
        public string ReadOutlookData()
        {
            string returnValue = null;
            Outlook.Application oApp;
            Outlook.NameSpace oNS;
            Outlook.MAPIFolder oCalendar;
            Outlook.Items calItems;

            List<Appointment> appointments = new List<Appointment>();

            try
            {
                // Create the Outlook application.
                oApp = new Outlook.Application();

                // Get the NameSpace and Logon information.                
                oNS = oApp.GetNamespace("MAPI");

                //Log on by using a dialog box to choose the profile.
                oNS.Logon(Missing.Value, Missing.Value, true, false);

                // Get the Calendar folder.
                oCalendar = oNS.GetDefaultFolder(Outlook.OlDefaultFolders.olFolderCalendar);

                DateTime startTime = DateTime.Today;
                DateTime endTime = startTime.AddDays(1);

                string startTimeStr = startTime.ToString("g");
                string endTimeStr = endTime.ToString("g");
                string filter = "[Start] <= '" + endTimeStr + "' AND [End] >= '" + startTimeStr + "'";

                // Get the Items (Appointments) collection from the Calendar folder.
                calItems = oCalendar.Items;
                calItems.IncludeRecurrences = true;
                calItems.Sort("[Start]", Type.Missing);
                Outlook.Items restrictItems = calItems.Restrict(filter);

                string subject, organizer, location= null;
                DateTime start, end;
                int remindertime=0;

                Appointment appt = null;

                foreach (Outlook.AppointmentItem oAppt in restrictItems)
                {
                    organizer = oAppt.Organizer;
                    subject = oAppt.Subject;
                    location = oAppt.Location;                                      

                    start = oAppt.Start;
                    end = oAppt.End;
                    remindertime = oAppt.ReminderMinutesBeforeStart;

                    appt = new Appointment(subject, location,organizer, start, end, remindertime);
                    appointments.Add(appt);
                }

                oNS.Logoff();
                returnValue = new JavaScriptSerializer().Serialize(appointments);
            }
            //Simple error handling.
            catch (Exception e)
            {
                
            }
            finally
            {
                // Clean up.                
                calItems = null;
                oCalendar = null;
                oNS = null;
                oApp = null;
            }

            return returnValue;
        }
    }
}
