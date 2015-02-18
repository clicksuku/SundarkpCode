namespace OutlookGCMService
{
    partial class OutlookSyncBYODService
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(OutlookSyncBYODService));
            this.timerSend = new System.Windows.Forms.Timer(this.components);
            this.notifyIcon1 = new System.Windows.Forms.NotifyIcon(this.components);
            this.ctxMenuOptions = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.restoreToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.exitToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.Setup = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.StatusText = new System.Windows.Forms.Label();
            this.RegIdText = new System.Windows.Forms.TextBox();
            this.ApiKeyText = new System.Windows.Forms.TextBox();
            this.Run = new System.Windows.Forms.Button();
            this.cbInterval = new System.Windows.Forms.ComboBox();
            this.label2 = new System.Windows.Forms.Label();
            this.EditProjID = new System.Windows.Forms.Button();
            this.EditRegID = new System.Windows.Forms.Button();
            this.ctxMenuOptions.SuspendLayout();
            this.SuspendLayout();
            // 
            // notifyIcon1
            // 
            this.notifyIcon1.ContextMenuStrip = this.ctxMenuOptions;
            this.notifyIcon1.Icon = ((System.Drawing.Icon)(resources.GetObject("notifyIcon1.Icon")));
            this.notifyIcon1.Text = "Outlook Meeting for Android";
            this.notifyIcon1.Visible = true;
            this.notifyIcon1.Click += new System.EventHandler(this.notifyIcon1_Click);
            this.notifyIcon1.DoubleClick += new System.EventHandler(this.notifyIcon1_DoubleClick);
            // 
            // ctxMenuOptions
            // 
            this.ctxMenuOptions.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.restoreToolStripMenuItem,
            this.exitToolStripMenuItem});
            this.ctxMenuOptions.Name = "ctxMenuOptions";
            this.ctxMenuOptions.Size = new System.Drawing.Size(114, 48);
            // 
            // restoreToolStripMenuItem
            // 
            this.restoreToolStripMenuItem.Name = "restoreToolStripMenuItem";
            this.restoreToolStripMenuItem.Size = new System.Drawing.Size(113, 22);
            this.restoreToolStripMenuItem.Text = "Restore";
            this.restoreToolStripMenuItem.Click += new System.EventHandler(this.restoreToolStripMenuItem_Click);
            // 
            // exitToolStripMenuItem
            // 
            this.exitToolStripMenuItem.Name = "exitToolStripMenuItem";
            this.exitToolStripMenuItem.Size = new System.Drawing.Size(113, 22);
            this.exitToolStripMenuItem.Text = "Exit";
            this.exitToolStripMenuItem.Click += new System.EventHandler(this.exitToolStripMenuItem_Click);
            // 
            // Setup
            // 
            this.Setup.Location = new System.Drawing.Point(167, 161);
            this.Setup.Name = "Setup";
            this.Setup.Size = new System.Drawing.Size(75, 23);
            this.Setup.TabIndex = 13;
            this.Setup.Text = "Setup";
            this.Setup.UseVisualStyleBackColor = true;
            this.Setup.Click += new System.EventHandler(this.Setup_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.ForeColor = System.Drawing.Color.Black;
            this.label1.Location = new System.Drawing.Point(80, 164);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(33, 13);
            this.label1.TabIndex = 12;
            this.label1.Text = "hours";
            // 
            // StatusText
            // 
            this.StatusText.AutoSize = true;
            this.StatusText.Font = new System.Drawing.Font("Arial Rounded MT Bold", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.StatusText.ForeColor = System.Drawing.SystemColors.ControlLight;
            this.StatusText.Location = new System.Drawing.Point(27, 203);
            this.StatusText.Name = "StatusText";
            this.StatusText.Size = new System.Drawing.Size(86, 12);
            this.StatusText.TabIndex = 10;
            this.StatusText.Text = "Current Status";
            this.StatusText.Visible = false;
            // 
            // RegIdText
            // 
            this.RegIdText.ForeColor = System.Drawing.SystemColors.GrayText;
            this.RegIdText.Location = new System.Drawing.Point(29, 80);
            this.RegIdText.Multiline = true;
            this.RegIdText.Name = "RegIdText";
            this.RegIdText.Size = new System.Drawing.Size(291, 69);
            this.RegIdText.TabIndex = 9;
            this.RegIdText.Text = "Enter Device Registration ID here";
            this.RegIdText.Enter += new System.EventHandler(this.RegIdText_Enter);
            // 
            // ApiKeyText
            // 
            this.ApiKeyText.ForeColor = System.Drawing.Color.Gray;
            this.ApiKeyText.Location = new System.Drawing.Point(29, 54);
            this.ApiKeyText.Name = "ApiKeyText";
            this.ApiKeyText.Size = new System.Drawing.Size(291, 20);
            this.ApiKeyText.TabIndex = 8;
            this.ApiKeyText.Text = "Enter Secret Key Here (Google Project)";
            this.ApiKeyText.Enter += new System.EventHandler(this.ApiKeyText_Enter);
            // 
            // Run
            // 
            this.Run.Location = new System.Drawing.Point(245, 161);
            this.Run.Name = "Run";
            this.Run.Size = new System.Drawing.Size(75, 23);
            this.Run.TabIndex = 15;
            this.Run.Text = "Run";
            this.Run.UseVisualStyleBackColor = true;
            this.Run.Click += new System.EventHandler(this.Run_Click);
            // 
            // cbInterval
            // 
            this.cbInterval.FormattingEnabled = true;
            this.cbInterval.Items.AddRange(new object[] {
            "1",
            "2",
            "3",
            "4"});
            this.cbInterval.Location = new System.Drawing.Point(29, 161);
            this.cbInterval.Name = "cbInterval";
            this.cbInterval.Size = new System.Drawing.Size(45, 21);
            this.cbInterval.TabIndex = 16;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.ForeColor = System.Drawing.SystemColors.ControlLight;
            this.label2.Location = new System.Drawing.Point(38, 20);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(271, 20);
            this.label2.TabIndex = 17;
            this.label2.Text = "OutlookSync for BYOD (Android)";
            // 
            // EditProjID
            // 
            this.EditProjID.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.EditProjID.Location = new System.Drawing.Point(326, 50);
            this.EditProjID.Name = "EditProjID";
            this.EditProjID.Size = new System.Drawing.Size(27, 27);
            this.EditProjID.TabIndex = 18;
            this.EditProjID.Text = "...";
            this.EditProjID.UseVisualStyleBackColor = true;
            this.EditProjID.Click += new System.EventHandler(this.EditProjID_Click);
            // 
            // EditRegID
            // 
            this.EditRegID.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.EditRegID.Location = new System.Drawing.Point(326, 83);
            this.EditRegID.Name = "EditRegID";
            this.EditRegID.Size = new System.Drawing.Size(27, 27);
            this.EditRegID.TabIndex = 19;
            this.EditRegID.Text = "...";
            this.EditRegID.UseVisualStyleBackColor = true;
            this.EditRegID.Click += new System.EventHandler(this.EditRegID_Click);
            // 
            // OutlookSyncBYODService
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(41)))), ((int)(((byte)(112)))), ((int)(((byte)(118)))));
            this.ClientSize = new System.Drawing.Size(365, 224);
            this.Controls.Add(this.EditRegID);
            this.Controls.Add(this.EditProjID);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.cbInterval);
            this.Controls.Add(this.Run);
            this.Controls.Add(this.Setup);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.StatusText);
            this.Controls.Add(this.RegIdText);
            this.Controls.Add(this.ApiKeyText);
            this.ForeColor = System.Drawing.Color.Black;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MaximizeBox = false;
            this.Name = "OutlookSyncBYODService";
            this.ShowInTaskbar = false;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Outlook Meetings on Phone";
            this.Resize += new System.EventHandler(this.OutlookGCMServiceForm_Resize);
            this.ctxMenuOptions.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Timer timerSend;
        private System.Windows.Forms.NotifyIcon notifyIcon1;
        private System.Windows.Forms.ContextMenuStrip ctxMenuOptions;
        private System.Windows.Forms.ToolStripMenuItem restoreToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem exitToolStripMenuItem;
        private System.Windows.Forms.Button Setup;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label StatusText;
        private System.Windows.Forms.TextBox RegIdText;
        private System.Windows.Forms.TextBox ApiKeyText;
        private System.Windows.Forms.Button Run;
        private System.Windows.Forms.ComboBox cbInterval;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button EditProjID;
        private System.Windows.Forms.Button EditRegID;
    }
}

