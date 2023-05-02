using BogusTestApp.Models;
using MahApps.Metro.Controls;
using Newtonsoft.Json;
using System.Windows;

namespace BogusTestApp
{
    /// <summary>
    /// MainWindow.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MainWindow : MetroWindow
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void BtnGenDummyData_Click(object sender, RoutedEventArgs e)
        {
            var repo = new SampleCustomerRepository();
            var customers = repo.GetCustomers(100);
            var result = JsonConvert.SerializeObject(customers, Formatting.Indented); // 들여쓰기 여부 Formatting.Indented
            RtbResult.Text = result;
        }
    }
}
