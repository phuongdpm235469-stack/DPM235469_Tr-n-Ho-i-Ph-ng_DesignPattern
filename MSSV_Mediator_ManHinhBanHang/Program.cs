Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== MEDIATOR: Điều phối màn hình bán hàng ===");
var screen = new SalesScreenMediator();
screen.Qty = new QuantityBox(screen);
screen.Total = new TotalLabel();
screen.Pay = new PayButton();
screen.Customer = new CustomerBox(screen);

screen.Qty.UnitPrice = 250000;
screen.Qty.SetQty(0);
screen.Qty.SetQty(3);
screen.Customer.Select("VIP");
screen.Qty.SetQty(4);

public interface ISalesMediator { void Notify(object sender, string ev); }
public class QuantityBox
{
    private readonly ISalesMediator _m; public int Qty; public decimal UnitPrice;
    public QuantityBox(ISalesMediator m) => _m = m;
    public void SetQty(int q) { Console.WriteLine($"> Nhập số lượng = {q}"); Qty = q; _m.Notify(this, "QtyChanged"); }
}
public class CustomerBox
{
    private readonly ISalesMediator _m; public string Type = "Thường";
    public CustomerBox(ISalesMediator m) => _m = m;
    public void Select(string t) { Console.WriteLine($"> Chọn khách hàng loại {t}"); Type = t; _m.Notify(this, "CustomerChanged"); }
}
public class TotalLabel { public void Show(decimal v) => Console.WriteLine($"   [Label] Thành tiền: {v:N0}"); }
public class PayButton { public void SetEnabled(bool e) => Console.WriteLine($"   [Nút Thanh toán] {(e ? "BẬT" : "TẮT")}"); }

public class SalesScreenMediator : ISalesMediator
{
    public QuantityBox Qty; public TotalLabel Total; public PayButton Pay; public CustomerBox Customer;
    public void Notify(object sender, string ev)
    {
        if (ev == "QtyChanged" || ev == "CustomerChanged")
        {
            var sum = Qty.Qty * Qty.UnitPrice;
            if (Customer.Type == "VIP") sum *= 0.9m;
            Total.Show(sum);
            Pay.SetEnabled(Qty.Qty > 0);
        }
    }
}
