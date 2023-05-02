using Bogus;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BogusTestApp.Models
{
    public class SampleCustomerRepository
    {
        public IEnumerable<Customer> GetCustomers(int genNumber)
        {
            Randomizer.Seed = new Random(123456); // Seed 갯수를 지정 숫자는 우리 마음대로 지정
            // 아래와 같은 규칙으로 주문 더미 데이터를 생성하겠다
            var orderGen = new Faker<Order>()
                .RuleFor(o => o.Id, Guid.NewGuid) // Id 값은 Guid로 자동 생성(
                .RuleFor(o => o.Date, f => f.Date.Past(3)) // 날짜를 3년전으로 세팅 설정
                .RuleFor(o => o.OrderValue, f => f.Finance.Amount(0, 10000)) // 1부터 10000까지 랜덤하게 생성
                .RuleFor(o => o.Shipped, f => f.Random.Bool(0.8f)); // true가 80프로 false가 20프로

            // 고객 더미 데이터 생성규칙
            var customerGen = new Faker<Customer>()
                .RuleFor(c => c.Id, Guid.NewGuid())
                .RuleFor(c => c.Name, f => f.Company.CompanyName())
                .RuleFor(c => c.Address, f => f.Address.FullAddress())
                .RuleFor(c => c.Phone, f => f.Phone.PhoneNumber())
                .RuleFor(c => c.ContectName, f => f.Name.FullName())
                .RuleFor(c => c.Orders, f => orderGen.Generate(f.Random.Number(1, 2)).ToList());

            return customerGen.Generate(genNumber); // n개의 가짜 고객 데이터를 생성해서 리턴
        }
    }
}
