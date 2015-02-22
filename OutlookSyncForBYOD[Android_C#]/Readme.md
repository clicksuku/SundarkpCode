##About this tool##

This tool sync Outlook Meetings(Basic Info only) to a non-Company-Owned Android Device. The tool leverages Google Cloud Messaging for Android to implement the 
sync. 

Outlook Sync is supported on Company-Owned Devices but it is not provided to everyone in the company. Google Calendar sync was an option but was not sure 
whether it would support syncing only the basic information. Basic Information used
	1. Meeting Subject
	2. Meeting Organizer
	3. Meeting Location
	4. Meeting Start Time
	5. Meeting End Time
	6. Meeting Reminder

##Few more details##

  1. **Why Google Cloud Messaging?**
     -Required a HTTP Way to automatically push the outlook meetings information to a custom Android Device. 
  
  
	 -![alt text](https://github.com/clicksuku/SundarkpCode/blob/master/Images/OutlookSyncServiceForBYOD_Design.png "Solution Design")	 
     
##Steps to Install##

###Pre-Requisites###
  
1. A Google Project with GCM Enabled is required
	a.	To enable Google Cloud Messaging between Windows Service and Android phone, create a project in [Google Developers Console](https://console.developers.google.com/project). 
	b.	Under the “API & Auth”, in APIs, enable ‘Google Cloud Messaging for Android’
	c.	Under “Credentials”, select ‘Create New Key’ (Public API Access). Choose “Server Key”
2.	Collect the following parameters
	a.	Get the ‘API Key’ from step 1.C 
	b.	Get the “Project Number” from “Overview” in the Project Created in step 1.
3. Microsoft Dotnet Framework 4.0


###Installation###
  
1.	Go to the [Link to download](https://drive.google.com/folderview?id=0BxO_wd5xBtRWfjJxNVlzTURtWlRtcXdSdTZXQkoyZjZ1MmRISk5GS3h4QVdQX2FoeVdLekk&usp=sharing_eid&invite=CO_E0ik)
2.	Android Client
	a.	Download OutlookSyncBYOD.apk
	b.	Install the apk using adb command
		i. adb install OutlookSyncBYOD.apk
3.	Windows Application (System Tray)
	a.	Goto OutlookSyncService
	b.	Download OutlookSyncByodInstaller.msi
	c.	Install msi

     
##How to Run##
1.	Android Side
	a.	Start the App	
	b.	Key in the Project Number (first Text Box) from 2.b in Perquisites. Click ‘Set’ to set the project ID.		
	c.	Click “Generate”. Device ID is generated
	d.	Mail the generated Device ID		
2.	Windows Service
	a.	Enter the ‘API Key’ obtained from ‘2.a’ in Perquisites
	b.	Enter the Device ID from the mail sent in 1.d above from Android
	c.	Click Setup (Please note that it is a one-Time Process. It should run automatically in the system tray)
	d.	Run			
3.	Android
	a.	Meetings are created
	b.	Reminders are automatically created in the calendar. 
	

##Screenshots##	

	![Landing Page](/https://github.com/clicksuku/SundarkpCode/blob/master/Images/OutlookBYODLandingPage.png )
    ![Device ID Generated](/https://github.com/clicksuku/SundarkpCode/blob/master/Images/OutlookBYODSetupScreen.png )
	![Mail the Device ID](/https://github.com/clicksuku/SundarkpCode/blob/master/Images/OutlookBYODDeviceID.png)
	![Windows Application](/https://github.com/clicksuku/SundarkpCode/blob/master/Images/OutlookBYODWinApp.png )
	
	![Meetings listed on your device](/https://github.com/clicksuku/SundarkpCode/blob/master/Images/OutlookBYODMeeting.png )
	
##Additional Info##
The data flowing over the GCM is encrypted with AES-128 algorithm. 

#License#
New APACHE License - Copyright(c) 2014, Sundara Kumar Padmanabhan. 
See [License](http://www.apache.org/licenses/LICENSE-2.0.html) for details.
    
##References##

    A.	Android GCM is mostly derived from http://hmkcode.com/android-google-cloud-messaging-tutorial/
	B.	Android – Swipe Gestures - http://stackoverflow.com/questions/4139288/android-how-to-handle-right-to-left-swipe-gestures
	C.	Encryption of Data over GCM - https://zenu.wordpress.com/2011/09/21/aes-128bit-cross-platform-java-and-c-encryption-compatibility/
	D.	Why the OutlookSyncService cannot run as a Windows Service? - https://support.microsoft.com/kb/237913 	

     
     
