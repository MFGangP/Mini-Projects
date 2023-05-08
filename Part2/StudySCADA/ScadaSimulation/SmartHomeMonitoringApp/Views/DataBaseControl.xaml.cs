using MahApps.Metro.Controls;
using MySql.Data.MySqlClient;
using Newtonsoft.Json;
using SmartHomeMonitoringApp.Logics;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using uPLibrary.Networking.M2Mqtt.Messages;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// DataBaseControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class DataBaseControl : UserControl
    {
        //진짜 접속이 된 건지 확인
        public bool IsConnected { get; set; }
        public DataBaseControl()
        {
            InitializeComponent();
        }
        // 유저 컨트롤 로드 이벤트 핸들러
        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            TxbBrokerUrl.Text = Commons.BROKERHOST;
            TxbMqttTopic.Text = Commons.MQTTTOPIC;
            TxbConnString.Text = Commons.MYSQL_CONNSTRING;

            IsConnected = false; // 아직 접속 안되있음.
            BtnConnDb.IsChecked = false; // 클릭하면 체크 true
        }

        // 토글이기 때문에 체크 (1:접속/2:접속 끊기) 이벤트 핸들러
        private void BtnConnDb_Click(object sender, RoutedEventArgs e)
        {
            if (IsConnected == false)
            {
                // MQTT 브로커 생성
                Commons.MQTT_CLIENT = new uPLibrary.Networking.M2Mqtt.MqttClient(Commons.BROKERHOST);
                // MQTT를 쓰기 위한 중요한 사항
                try
                {
                    // MQTT subscribe(구독할) 로직
                    if (Commons.MQTT_CLIENT.IsConnected == false)
                    {
                        // MQTT 접속 시도
                        Commons.MQTT_CLIENT.MqttMsgPublishReceived += MQTT_CLIENT_MqttMsgPublishReceived;
                        Commons.MQTT_CLIENT.Connect("MONITOR");
                        Commons.MQTT_CLIENT.Subscribe(new string[] { Commons.MQTTTOPIC },
                                new byte[] { MqttMsgBase.QOS_LEVEL_AT_MOST_ONCE }); // QOS는 네트워크 통신의 옵션
                        UpdateLog(">>> MQTT Broker Connected");


                        BtnConnDb.IsChecked = true;
                        IsConnected = true; // 예외 발생하면 true로 변경할 필요 없음.
                    }
                }
                catch (Exception ex)
                {

                    //
                }
            }
            else
            {
                BtnConnDb.IsChecked = false;
                IsConnected = false;
            }
        }

        private void UpdateLog(string msg)
        {
            // 예외처리 필요!!
            this.Invoke(() => {
                TxtLog.Text += $"{msg}\n";
                TxtLog.ScrollToEnd();
            });
        }
        // Subscribe가 발생할 때 이벤트 핸들러
        private void MQTT_CLIENT_MqttMsgPublishReceived(object sender, MqttMsgPublishEventArgs e)
        {
            // 받을 때 바이트로 받았기 때문에 스트링으로 바꿔줘야 된다.
            var msg = Encoding.Default.GetString(e.Message);
            UpdateLog(msg);

            SetToDataBase(msg, e.Topic); // 실제 DB에 저장처리
        }

        // DB 저장 처리 메서드
        private void SetToDataBase(string msg, string topic)
        {
            // 지금 들어온 메시지를 바꿔줌
            var currValue = JsonConvert.DeserializeObject<Dictionary<string, string>>(msg);
            if (currValue != null)
            {
                //Debug.WriteLine(currValue["Home_Id"]);
                //Debug.WriteLine(currValue["RoomName"]);
                //Debug.WriteLine(currValue["Sensing_Datetime"]);
                //Debug.WriteLine(currValue["Temp"]);
                //Debug.WriteLine(currValue["Humid"]);
                try
                {
                    using (MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING)
                    { 
                        if (conn.State == System.Data.ConnectionState.Closed) conn.Open();
                        string insQuery = "INSERT INTO smarthomesensor.....";

                        MySqlCommand cmd = new MySqlCommand(insQuery, conn);
                        cmd.Parameters.AddWithValue("@Home_Id", currValue["Home_Id"]);

                        //..파라미터 다섯개
                        if (cmd.ExecuteNonQuery() == 1)
                        {
                            UpdateLog(">>> DB Insert succeed.");
                        }
                        else
                        {
                            UpdateLog(">>> DB Insert Failed."); // 일어날 일이 거의 없음
                        }
                        }
                }    
                catch (Exception ex)
                {
                    UpdateLog($">>> Error 발생 : {ex.Message}");
                }
            }
        }
    }
}

