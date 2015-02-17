using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;

using System.Windows.Forms;
using System.Timers;

namespace OutlookGCMService
{
    
    public partial class OutlookSyncBYODService : Form
    {
        /*private const int CP_NOCLOSE_BUTTON = 0x200;
        protected override CreateParams CreateParams
        {
            get
            {
                CreateParams myCp = base.CreateParams;
                myCp.ClassStyle = myCp.ClassStyle | CP_NOCLOSE_BUTTON;
                return myCp;
            }
        }*/

        private SendData _sendData = new SendData();
        private int interval = 0;
        private string _lastcachedString;

        public OutlookSyncBYODService()
        {
            InitializeComponent();
            interval = 2;

            cbInterval.SelectedIndex = 0;
            timerSend.Tick += new EventHandler(timerSend_Tick);
            cbInterval.Focus();
            this.ShowInTaskbar = true;
        }
                   

        private void ApiKeyText_Enter(object sender, EventArgs e)
        {
            ApiKeyText.ForeColor = Color.Black;
            ApiKeyText.Text = "";
            StatusText.Visible = false;
        }

        private void RegIdText_Enter(object sender, EventArgs e)
        {
            RegIdText.ForeColor = Color.Black;
            RegIdText.Text = "";
            StatusText.Visible = false;
        }             

        private void Setup_Click(object sender, EventArgs e)
        {
            if ((ApiKeyText.Text == null) || (RegIdText.Text == null) ||
               (ApiKeyText.Text.Length == 0) || (RegIdText.Text.Length == 0))
            {
                MessageBox.Show("Please Enter data");
                return;
            }

            int num = Convert.ToInt16(cbInterval.Text);
            if ((num > 0) || (num <= 4))
                interval = num;           

            timerSend.Interval = interval * 60 * 60 * 1000;    //Interval should be in milliseconds (hours to milli conversion) 

            _sendData.ApiKey = ApiKeyText.Text;
            _sendData.RegistrationId = RegIdText.Text;

            StatusText.Visible = true;
            StatusText.Text = "Properties are set Successfully";
        }

        private void Run_Click(object sender, EventArgs e)
        {
            if ((_sendData.ApiKey == null) || (_sendData.RegistrationId == null) ||
                (_sendData.ApiKey.Length == 0) || (_sendData.RegistrationId.Length == 0))
            {
                MessageBox.Show("Please set API Secret Key and Device RegID before starting.");
                return;
            }

            MessageBox.Show("Started Running");

            OutlookRead oRead = new OutlookRead();
            string data = oRead.ReadOutlookData();

            string response = _sendData.Send(data);
            _lastcachedString = data;

            timerSend.Interval = interval * 1000;
            timerSend.Enabled = true;
        } 


        //Timer Functions

        void timerSend_Tick(object sender, EventArgs e)
        {
            OutlookRead oRead = new OutlookRead();
            string data = oRead.ReadOutlookData();

            if (_lastcachedString != data)
            {
                string response = _sendData.Send(data);
                _lastcachedString = data;
            }            
        }

        private void OutlookGCMServiceForm_Resize(object sender, EventArgs e)
        {
            if (FormWindowState.Minimized == WindowState)
            {
                this.ShowInTaskbar = false;
                Hide();
            }
        }


        //Notify Icon and 

        private void notifyIcon1_DoubleClick(object sender, EventArgs e)
        {
            Show();
            this.ShowInTaskbar = true;
            WindowState = FormWindowState.Normal;
        }

        private void restoreToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Show();
            this.ShowInTaskbar = true;
            WindowState = FormWindowState.Normal;
        }

        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Close();
        }
               

        private void notifyIcon1_Click(object sender, EventArgs e)
        {
            int x = Cursor.Position.X;
            int y = Cursor.Position.Y;
                        
            y = y - 30;

            ctxMenuOptions.Show(new Point(x,y));
        }       
    }
}
