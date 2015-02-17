using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using System.Net;
using System.Security.Cryptography;

namespace OutlookGCMService
{
    class SendData
    {
        private string _apikey;
        private string _regId;
        private EncryptionUtility encryptor = new EncryptionUtility();

        
        public string ApiKey
        {
            set { _apikey = value; }
            get { return _apikey; }
        }

        public string RegistrationId
        {
            set { _regId = value; } 
            get { return _regId; }
        }

        public string Send(string data)
        {
            try
            {
                string URI = "https://android.googleapis.com/gcm/send";
                WebRequest req = WebRequest.Create(URI);

                req.ContentType = "application/json";
                string apiKey = ApiKey;
                req.Headers.Add("Authorization", "key=" + apiKey);
                req.Method = "POST";


                String encryptedData = encryptor.Encrypt(data, "123");
                data = "{\"meetings\":\"" + encryptedData + "\"}";

                
                string sendData = "{\"registration_ids\":[\"" + RegistrationId + "\"],\"data\":" + data + "}";           
                
                byte[] bytes = System.Text.Encoding.ASCII.GetBytes(sendData);
                req.ContentLength = bytes.Length;
                System.IO.Stream os = req.GetRequestStream();
                os.Write(bytes, 0, bytes.Length); //Push it out there
                os.Close();

                System.Net.WebResponse resp = req.GetResponse();
                if (resp == null) return null;

                System.IO.StreamReader sr = new System.IO.StreamReader(resp.GetResponseStream());
                string response = sr.ReadToEnd().Trim();
                return response;
            }
            catch (System.Exception ex)
            {
                return null;	
            }            
        }
    }
}
