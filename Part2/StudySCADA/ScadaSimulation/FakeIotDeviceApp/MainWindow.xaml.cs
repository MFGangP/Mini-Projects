using Bogus;
using FakeIotDeviceApp.Models;
using MahApps.Metro.Controls;
using MahApps.Metro.Controls.Dialogs;
using Newtonsoft.Json;
using System;
using System.Diagnostics;
using System.Text;
using System.Threading;
using System.Windows;
using System.Windows.Documents;
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

        Faker<SensorInfo> FakeHomeSensor { get; set; } = null; // 가짜 스마트홈 센서 값 변수

        MqttClient Client;
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
        // 핵심 처리 - 센싱된 데이터 값을 MQTT 브로커로 전송
        private void StartPublish()
        {

            MqttThread = new Thread(() =>
            {
                while (true)
                {
                    // 가짜 스마트 홈 센서값을 생성
                    SensorInfo Info = FakeHomeSensor.Generate();
                    // 릴리즈(배포) 때는 주석처리 / 삭제
                    Debug.WriteLine($"{Info.Home_Id} / {Info.RoomName} / {Info.Sensing_Datetime} / {Info.Temp}");
                    // 객체 직렬화 (객체 데이터를 xml이나 json등의 문자열로 만들어주는걸 말한다)
                    var jsonValue = JsonConvert.SerializeObject(Info, Formatting.Indented); // XmlConvert면 xml로 뒤에 Formatting.Indented는 들여쓰기 해주는 역할
                    // 센서값 MQTT 브로커에 전송 (Publish)
                    // TCP/IP 통신에서 그냥 보내면 다 깨지니까 인코딩을 바이트 값으로 해줘야된다.
                    Client.Publish("SmartHome/IotData/",Encoding.Default.GetBytes(jsonValue));
                    // RtbLog에 출력 - 스레드와 UI 스레드간 충돌이 안나도록 변경 
                    this.Invoke(new Action(() => { // 여기는 우리가 생성한거 로그에 바로 찍어주는거.
                        // 이대로 보내면 문제 생긴다
                        RtbLog.AppendText($"{jsonValue}\n");
                        RtbLog.ScrollToEnd(); // 이걸 빼면 우리가 직접 스크롤을 내려야 된다.
                    }));

                    // 1초 동안 대기
                    Thread.Sleep(1000);
                }
            });
            MqttThread.Start();
        }

        private void ConnectMqttBroker()
        {
            Client = new MqttClient(TxtMqttBrokerIp.Text);
            Client.Connect("SmartHomeDev"); // publish Client ID를 지정
        }
        private void MetroWindow_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            if(Client.IsConnected == true && Client != null)
            {
                Client.Disconnect(); // 접속을 끊어주고
            }
            if (MqttThread != null)
            {
                MqttThread.Abort(); // 여기가 없으면 프로그램 종료 후에도 메모리에 남아있음.
            }
        }
    }
}
