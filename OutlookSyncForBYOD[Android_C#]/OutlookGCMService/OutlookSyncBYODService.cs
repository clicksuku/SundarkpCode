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
        private SendData _sendData;
        private int interval = 0;
        private string _lastcachedString;
        private static bool IsFirstTime = true;
        private static int DataSentTimes = 0;
        

        public OutlookSyncBYODService()
        {
            InitializeComponent();
            interval = 1;

            cbInterval.SelectedIndex = 0;
            timerSend.Tick += new EventHandler(timerSend_Tick);
            cbInterval.Focus();
            
            this.Resize += new EventHandler(Form1_Resize);
            this.Load += new EventHandler(Form1_Load);            
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            
            bool isRead = ConfigFileOperations.ReadXML(ref _sendData);            

            if (isRead)
            {
                InitializeFields();
                Run.PerformClick();
            }
            else
            {
                _sendData = new SendData();
            }
            WindowState = FormWindowState.Minimized;
        }

        private void Form1_Resize(object sender, EventArgs e)
        {
            if (WindowState == FormWindowState.Minimized)
            {
                ShowInTaskbar = false;
                Hide();
            }
            else if (WindowState == FormWindowState.Normal)
            {
                ShowInTaskbar = true;
                Show();
            }
        }

        private void InitializeFields()
        {
            ApiKeyText.ForeColor = Color.Black;
            ApiKeyText.Text = _sendData.ApiKey;
            ApiKeyText.Enabled = false;

            RegIdText.ForeColor = Color.Black;
            RegIdText.Text = _sendData.RegistrationId;
            RegIdText.Enabled = false;
            cbInterval.SelectedIndex = _sendData.RunningInterval - 1;
            StatusText.Visible = true;
            StatusText.Text = "Data sent to GCM  :  " + _sendData.NumberTimes.ToString() + "  times";

            IsFirstTime = false;
            Setup.Enabled = false;
        }

        private void ApiKeyText_Enter(object sender, EventArgs e)
        {
            if (IsFirstTime)
            {
                ApiKeyText.ForeColor = Color.Black;
                ApiKeyText.Text = "";
                StatusText.Visible = false;
            }
        }

        private void RegIdText_Enter(object sender, EventArgs e)
        {
            if (IsFirstTime)
            {
                RegIdText.ForeColor = Color.Black;
                RegIdText.Text = "";
                StatusText.Visible = false;
            }
            
        }             

        private void Setup_Click(object sender, EventArgs e)
        {
            if ((ApiKeyText.Text == null) || (RegIdText.Text == null) ||
               (ApiKeyText.Text.Length == 0) || (RegIdText.Text.Length == 0))
            {
                MessageBox.Show("Please Enter data");
                return;
            }

            ApiKeyText.Enabled = false;
            RegIdText.Enabled = false;

            int num = Convert.ToInt16(cbInterval.Text);
            if ((num > 0) || (num <= 4))
            {
                interval = num;
            }

            if (_sendData == null)
            {
                _sendData = new SendData();    
            }

            _sendData.RunningInterval = interval;
            _sendData.ApiKey = ApiKeyText.Text;
            _sendData.RegistrationId = RegIdText.Text;
            _sendData.NumberTimes = DataSentTimes;

            IsFirstTime = false;

            StatusText.Visible = true;
            StatusText.Text = "Properties are set Successfully";
            timerSend.Stop();

            ConfigFileOperations.WriteXML(_sendData);
            Setup.Enabled = false;
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

            bool response = _sendData.Send(data);

            if (!response)
            {
                restoreToolStripMenuItem.PerformClick();
            }
            else
            {
                _lastcachedString = data;
                DataSentTimes++;                             
            }

            StatusText.Visible = true;   
            StatusText.Text = "Data sent to GCM  :  " + DataSentTimes.ToString() + "  times";            

            timerSend.Interval = interval * 60 * 60 * 1000;    //Interval should be in milliseconds (hours to milli conversion)             
            timerSend.Enabled = true;
            timerSend.Start();
        }

        private void EditProjID_Click(object sender, EventArgs e)
        {
            ApiKeyText.Enabled = true;
            StatusText.Visible = false;
            Setup.Enabled = true;
        }

        private void EditRegID_Click(object sender, EventArgs e)
        {
            RegIdText.Enabled = true;
            StatusText.Visible = false;
            Setup.Enabled = true;
        }

        //Timer Functions

        void timerSend_Tick(object sender, EventArgs e)
        {
            OutlookRead oRead = new OutlookRead();
            string data = oRead.ReadOutlookData();

            if (_lastcachedString != data)
            {
                bool response = _sendData.Send(data);
                if (!response)
                {

                }
                else
                {
                    _lastcachedString = data;
                    DataSentTimes++;                
                }
                
                _sendData.NumberTimes = DataSentTimes;
                StatusText.Visible = true;
                StatusText.Text = "Data sent to GCM  :  " + DataSentTimes.ToString() + "  times";                   
            }            
        }


        //Notify Icon 

        private void notifyIcon1_DoubleClick(object sender, EventArgs e)
        {
            try
            {
                Show();     
                this.WindowState = FormWindowState.Normal;
            }
            catch (Exception ex)
            {
                string message = ex.Message;
            }
        }

        private void restoreToolStripMenuItem_Click(object sender, EventArgs e)
        {
            try
            {
                Show();
                this.WindowState = FormWindowState.Normal;
            }
            catch (Exception ex)
            {
                string message = ex.Message;
            }
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

        private void OutlookSyncBYODService_FormClosed(object sender, FormClosedEventArgs e)
        {
            ConfigFileOperations.WriteXML(_sendData);
        }             
    }
}
