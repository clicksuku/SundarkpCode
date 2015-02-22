using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace OutlookGCMService
{
    internal class Appointment
    {
        private string _subject;
        private string _location;        
        private string _organizer;

        private string _starttime;
        private string _endtime;
        private int _reminder;

        public string Subject
        {
            get
            {
                return _subject;
            }
            set
            {
                _subject = value;
            }
        }
        
        public string Location
        {
            get
            {
                return _location;
            }
            set
            {
                _location = value;
            }
        }       

        public string Organizer
        {
            get
            {
                return _organizer;
            }
            set
            {
                _organizer = value;
            }
        }

        public string Start
        {
            get
            {
                return _starttime;
            }
            set
            {
                _starttime = value;
            }
        }

        public string End
        {
            get
            {
                return _endtime;
            }
            set
            {
                _endtime = value;
            }
        }

        public int Reminder
        {
            get
            {
                return _reminder;
            }
            set
            {
                _reminder = value;
            }
        }

        public Appointment(string subject, string location, string organizer, DateTime start,
                            DateTime end, int reminder)
        {
            Subject = subject;
            Location = location;            
            Organizer = organizer;

            Start = start.ToString("dd/MM/yyyy HH:mm:ss");
            End = end.ToString("dd/MM/yyyy HH:mm:ss");
            Reminder = reminder;

        }
        

    }
}
