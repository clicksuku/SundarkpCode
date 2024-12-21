using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Xml;

namespace OutlookGCMService
{
    class ConfigFileOperations
    {
        public ConfigFileOperations()
        {

        }

        public static bool WriteXML(SendData sendData)
        {
            System.Xml.Serialization.XmlSerializer writer;

            try
            {
                writer = new System.Xml.Serialization.XmlSerializer(typeof(SendData));
                System.IO.StreamWriter file = new System.IO.StreamWriter(@"Config.dat");
                writer.Serialize(file, sendData);
                file.Close();
                return true;
            }
            catch (Exception ex)
            {
                return false;
            }
            finally
            {

            }
        }

        public static bool ReadXML(ref SendData sendData)
        {
            System.Xml.Serialization.XmlSerializer reader;
            
            try
            {
                reader = new System.Xml.Serialization.XmlSerializer(typeof(SendData));
                System.IO.StreamReader file = new System.IO.StreamReader(@"Config.dat");
                sendData = new SendData();
                sendData = (SendData)reader.Deserialize(file);
                file.Close();
                return true;
            }
            catch (Exception ex)
            {
                return false;
            }
            finally
            {
                
            }            
        }

    }
}
