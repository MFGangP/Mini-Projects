using System;

namespace FakeIotDeviceApp.Models
{
    public class SensorInfo
    {
        public string Home_Id { get; set; } // 몇 동 몇 호D101H101 D101H102
        public string RoomName { get; set; } // 방 이름 Living, Dinning, Bed, Bath 
        public DateTime Sensing_Datetime { get; set; } // 센싱되는 현재 시각
        public float Temp { get ; set; } // 온도
        public float Humid { get; set; } // 습도
    }
}
