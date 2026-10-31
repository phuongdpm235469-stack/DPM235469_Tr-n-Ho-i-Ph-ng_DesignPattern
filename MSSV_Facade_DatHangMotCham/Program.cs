Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== FACADE: Nút Đặt hàng 1-chạm ===");
var facade = new CheckoutFacade(new InventoryService(), new PaymentService(), new ShippingService(), new NotificationService());

var ok = new CheckoutOrder { Id = "DH01", Customer = "An", Product = "iPhone", Qty = 1, Total = 20_000_000 };
Console.WriteLine($"=> Kết quả: {(facade.PlaceOrder(ok) ? "THÀNH CÔNG" : "THẤT BẠI")}\n");

var fail = new CheckoutOrder { Id = "DH02", Customer = "Bình", Product = "iPhone", Qty = 999, Total = 1_000_000 };
Console.WriteLine($"=> Kết quả: {(facade.PlaceOrder(fail) ? "THÀNH CÔNG" : "THẤT BẠI")}");

public class CheckoutOrder { public string Id, Customer, Product; public int Qty; public decimal Total; }

public class InventoryService
{
    private int _stock = 10;
    public bool ReserveStock(CheckoutOrder o) { if (o.Qty > _stock) { Console.WriteLine("  [Kho] Không đủ hàng."); return false; } _stock -= o.Qty; Console.WriteLine($"  [Kho] Đã giữ {o.Qty} {o.Product}."); return true; }
    public void Release(CheckoutOrder o) { _stock += o.Qty; Console.WriteLine("  [Kho] Hoàn kho."); }
}
public class PaymentService { public bool Charge(string c, decimal amt) { Console.WriteLine($"  [Ví] Trừ {amt:N0} của {c}."); return true; } }
public class ShippingService { public string CreateWaybill(CheckoutOrder o) { var w = "VD-" + o.Id; Console.WriteLine($"  [Vận chuyển] Tạo vận đơn {w}."); return w; } }
public class NotificationService { public void Send(string c, string msg) => Console.WriteLine($"  [SMS/Email] Gửi {c}: {msg}"); }

public class CheckoutFacade
{
    private readonly InventoryService _inv; private readonly PaymentService _pay;
    private readonly ShippingService _ship; private readonly NotificationService _noti;
    public CheckoutFacade(InventoryService i, PaymentService p, ShippingService s, NotificationService n) { _inv = i; _pay = p; _ship = s; _noti = n; }

    public bool PlaceOrder(CheckoutOrder order)   // Client chỉ gọi 1 phương thức duy nhất
    {
        Console.WriteLine($"Đặt hàng {order.Id}...");
        if (!_inv.ReserveStock(order)) return false;
        if (!_pay.Charge(order.Customer, order.Total)) { _inv.Release(order); return false; }
        var waybill = _ship.CreateWaybill(order);
        _noti.Send(order.Customer, $"Đơn {order.Id} thành công, vận đơn {waybill}");
        return true;
    }
}
