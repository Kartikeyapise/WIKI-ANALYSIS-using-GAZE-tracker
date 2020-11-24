using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using GazeFlowAPI;



namespace Client_GazeFlowAPI
{
    class Program
    {

        static void Main(string[] args)
        {


            CGazeFlowAPI gazeFlowAPI = new CGazeFlowAPI();


            //To get your AppKey register at http://gazeflow.epizy.com/GazeFlowAPI/register/

            string AppKey = "AppKeyDemo";

            if (gazeFlowAPI.Connect("127.0.0.1", 43333, AppKey))
            {
                string path = "./data.txt";      // write path to the data file to be created

                System.IO.File.Delete(@path);

                while (true)
                {
                    CGazeData GazeData = gazeFlowAPI.ReciveGazeDataSyn();
                    if (GazeData == null)
                    {
                        Console.WriteLine("Disconected");
                        return;
                    }
                    else
                    {

                        Console.WriteLine("Gaze: {0} , {1}", GazeData.GazeX, GazeData.GazeY);
                        Console.WriteLine("Head: {0} , {1}, {2}", GazeData.HeadX, GazeData.HeadY, GazeData.HeadZ);
                        Console.WriteLine("Head rot : {0} , {1}, {2}", GazeData.HeadYaw, GazeData.HeadPitch, GazeData.HeadRoll);
                        Console.WriteLine("");

                        AppendFile af = new AppendFile();
                        float gx=GazeData.GazeX,gy=GazeData.GazeY;
                        // string gxs=gx.ToString(),gys=gy.ToString();
                        af.Data(gx, gy, path);
                        // System.Threading.Thread.Sleep(500);
                    }
                }


            }
            else
            Console.WriteLine("Connection fail");
            Console.Read();

          
        }
    }
}