using MySql.Data.MySqlClient;
using OxyPlot;
using OxyPlot.Legends;
using OxyPlot.Series;
using SmartHomeMonitoringApp.Logics;
using System;
using System.Collections.Generic;
using System.Data;
using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;

namespace SmartHomeMonitoringApp.Views
{
    /// <summary>
    /// VisualizationControl.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class VisualizationControl : UserControl
    {
        List<string> Divisions = null;
        string FirstSensingDate = string.Empty;
        int TotalDateCount = 0; // 검색된 데이터 개수

        public VisualizationControl()
        {
            InitializeComponent();
        }

        private void UserControl_Loaded(object sender, RoutedEventArgs e)
        {
            Divisions = new List<string> { "SELECT", "LIVING", "DINING", "BED", "BATH" };
            CboRoomName.ItemsSource = Divisions;
            CboRoomName.SelectedIndex = 0; // SELECT가 기본 선택
            // 검색시작일 날짜 - DB에서 제일 오래된 날짜를 가져와서 할당
            using (MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
            {
                conn.Open();
                var dtQuery = $@"SELECT F.Sensing_Date
                                   FROM (
                                         SELECT DATE_FORMAT(Sensing_DateTime, '%Y-%m-%d') AS Sensing_Date
	                                     FROM smarthomesensor
	                                    )AS F
                                  GROUP BY F.Sensing_Date
                                  ORDER BY F.Sensing_Date ASC Limit 1;";
                MySqlCommand cmd = new MySqlCommand(dtQuery, conn);
                var result = cmd.ExecuteScalar();
                Debug.WriteLine(result.ToString());
                FirstSensingDate = DtpStart.Text = result.ToString();
                // 검색 종료일은 현재일자 할당
                DtpEnd.Text = DateTime.Now.ToString("yyyy-MM-dd");

            }
        }
        // 검색 버튼 클릭 이벤트 핸들러
        private async void BtnSearch_Click(object sender, RoutedEventArgs e)
        {
            // 검증 오류 한꺼번에 알려주는 방법
            bool isValid = true;
            string errorMsg = string.Empty;
            DataSet ds = new DataSet(); // DB 상에 있던 센싱데이터 담는 데이터 셋

            // 검색, 저장, 수정, 삭제 전 반드시 검증(Validation)
            if (CboRoomName.SelectedValue.ToString() == "SELECT")
            {
                isValid = false;
                errorMsg += "● 방 구분을 선택하세요.\n";
            }
            // 시스템 시작된 날짜보다 더 옛날 날짜로 검색하려면
            if (DateTime.Parse(DtpStart.Text) < DateTime.Parse(FirstSensingDate))
            {
                isValid = false;
                errorMsg += $"● 검색 시작일은 {FirstSensingDate}부터 가능합니다.\n";
            }
            // 오늘 날짜 이후의 날짜로 검색을 시도 할 때.
            if (DateTime.Parse(DtpEnd.Text) > DateTime.Now)
            {
                isValid = false;
                errorMsg += $"● 검색 종료일은 오늘까지 가능합니다.\n";
            }
            // 검색 시작일이 검색 종료일 보다 이후면
            if (DateTime.Parse(DtpStart.Text) > DateTime.Parse(DtpEnd.Text))
            {
                isValid = false;
                errorMsg += $"● 검색 시작일이 검색 종요일 보다 최신일 수 없습니다.\n";
            }
            if (isValid == false) 
            {
                await Commons.ShowCustomMessageAsync("검색", errorMsg);
                return;
            }
            // 검증 종료
            // 검색 시작
            TotalDateCount = 0;
            try
            {
                using (MySqlConnection conn = new MySqlConnection(Commons.MYSQL_CONNSTRING))
                {
                    conn.Open();
                    var searchQuery = $@"SELECT id,
                                                Home_Id,
                                                Room_Name,
                                                Sensing_Datetime,
                                                Temp,
                                                Humid
                                           FROM smarthomesensor
                                          WHERE UPPER(Room_Name) = @Room_Name
                                            AND DATE_FORMAT(Sensing_Datetime, '%Y-%m-%d') 
                                        BETWEEN @StartDate AND @EndDate;";
                    MySqlCommand cmd = new MySqlCommand(searchQuery, conn);
                    cmd.Parameters.AddWithValue("@Room_Name", CboRoomName.SelectedValue.ToString());
                    cmd.Parameters.AddWithValue("@StartDate", DtpStart.Text);
                    cmd.Parameters.AddWithValue("@EndDate", DtpEnd.Text);
                    MySqlDataAdapter adapter = new MySqlDataAdapter(cmd);

                    adapter.Fill(ds, "smarthomesensor");
                    // MessageBox.Show(ds.Tables["smarthomesensor"].Rows.Count.ToString(), "TotalData"); // 데이터 개수 확인
                }
            }
            catch (Exception ex)
            {
                await Commons.ShowCustomMessageAsync("DB 검색", $"DB 검색 오류 {ex.Message}");
            }

            // DB에서 가져온 데이터 차트에 뿌리도록 처리
            // Create two line series (markers are hidden by default)
            var tmp = new PlotModel { Title = $"{CboRoomName.SelectedValue} ROOM", DefaultFont="NanumGothic" };

            var legend = new Legend
            {
                LegendBorder = OxyColors.DarkGray,
                LegendBackground = OxyColor.FromArgb(150, 255, 255, 255),
                LegendPosition = LegendPosition.TopRight,
                LegendPlacement = LegendPlacement.Outside,
            };

            tmp.Legends.Add(legend); // 범례 추가

            var tempSeries = new LineSeries 
            { 
                Title = "Temperature(℃)", 
                MarkerType = MarkerType.Circle,
                Color = OxyColors.DarkOrange, // 라인 색상 온도는 주황색
            };
            var humidSeries = new LineSeries 
            { 
                Title = "Humidity(%)", 
                MarkerType = MarkerType.Square,
                Color = OxyColors.Aqua, // 습도는 아쿠아
            };

            if (ds.Tables[0].Rows.Count > 0)
            {
                TotalDateCount = ds.Tables[0].Rows.Count;

                var count = 0;
                foreach (DataRow row in ds.Tables[0].Rows)
                {
                    tempSeries.Points.Add(new DataPoint(count++, Convert.ToDouble(row["Temp"])));
                    humidSeries.Points.Add(new DataPoint(count++, Convert.ToDouble(row["Humid"])));
                    Convert.ToDouble(row["Temp"]); // 갯수 만큼 전부 다 담음
                }
            }
            // if 문 안에 들어가냐 마냐에 따라서 결과가 달라지니까 잘 봐야된다.
            // Add the series to the plot model
            tmp.Series.Add(tempSeries);
            tmp.Series.Add(humidSeries);

            OpvSmartHome.Model = tmp;

            LblTotalCount.Content = $"검색데이터 {TotalDateCount}개";
        }
    }
}
