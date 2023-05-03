using Bogus;
using FakeIotDeviceApp.Models;
using MahApps.Metro.Controls;
using MahApps.Metro.Controls.Dialogs;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading;
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
using uPLibrary.Networking.M2Mqtt;

namespace FakeIotDeviceApp
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : MetroWindow
    {
        public MainWindow()
        {
            InitializeComponent();
            InitFakeData();
        }

        Faker<SensorInfo> FakeHomeSensor = null; // 가짜 스마트홈 센서 값 변수

        MqttClient client;
        Thread MqttThread { get; set; }
        private void InitFakeData()
        {
            var Rooms = new[] { "Bed", "Bath", "Living", "Dining" };

            FakeHomeSensor = new Faker<SensorInfo>()
                .RuleFor(s => s.Home_Id, "D101H101") // 임의로 픽스된 스마트 홈 아이디
                .RuleFor(s => s.RoomName, f => f.PickRandom(Rooms)) // 실행 할 때마다 방이름이 계속 변경
                .RuleFor(s => s.Sensing_Datetime, f => f.Date.Past(0)) // 현재 시각이 생성
                .RuleFor(s => s.Temp, f => f.Random.Float(20.0f, 30.0f)) // 20~30도 사이의 실수값이 생성
                .RuleFor(s => s.Humid, f => f.Random.Float(40.0f, 64.0f)); // 40~64% 사이의 습도값

     
        }

        private async void BtnConnect_Click(object sender, RoutedEventArgs e)
        {
            if(string.IsNullOrEmpty(TxtMqttBrokerIp.Text))
            {
                await this.ShowMessageAsync("오류", $"브로커 아이피를 입력하세요");
                return;
            }

            // 브로커 아이피로 접속
            ConnectMqttBroker();
            // 하위의 로직을 무한 반복
            StartPublish();

        }

        private void StartPublish()
        {

            MqttThread = new Thread(() =>
            {
                while (true)
                {
                    // 가짜 스마트 홈 센서값을 생성
                    SensorInfo Info = FakeHomeSensor.Generate();
                    Debug.WriteLine($"{Info.Home_Id} / {Info.RoomName} / {Info.Sensing_Datetime} / {Info.Temp}");
                    // 센서값 MQTT 브로커에 전송 (Publish)

                    // RtbLog에 출력

                    // 1초 동안 대기
                    Thread.Sleep(1000);
                }
            });
            MqttThread.Start();
        }

        private void ConnectMqttBroker()
        {
            client = new MqttClient(TxtMqttBrokerIp.Text);
            client.Connect("SmartHomeDev"); // publish client ID를 지정
        }
        private void MetroWindow_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if(client.IsConnected == true && client != null)
            {
                client.Disconnect(); // 접속을 안 끊으면 메모리 상에 계속 남아있음!
            }
            if (MqttThread != null)
            {
                MqttThread.Abort();
            }
        }
    }
}
