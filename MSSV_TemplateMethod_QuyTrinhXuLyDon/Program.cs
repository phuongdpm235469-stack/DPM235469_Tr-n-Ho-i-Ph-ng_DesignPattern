Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== TEMPLATE METHOD: Quy trình xử lý đơn hàng ===");
OrderProcessor[] processors = { new RetailOrderProcessor(), new WholesaleOrderProcessor() };
foreach (var p in processors) { p.Process("HD-3001", 100); Console.WriteLine(); }

public abstract class OrderProcessor
{
    // Template method: khung quy trình cố định
    public void Process(string orderId, int qty)
    {
        Console.WriteLine($"--- {GetType().Name} xử lý {orderId} ---");
        Validate(orderId, qty);
        var price = CalculatePrice(qty);
        TakePayment(price);
        Ship(orderId);
        AfterSales(orderId);   // hook
    }
    protected void Validate(string id, int qty) => Console.WriteLine($"1. Kiểm tra đơn {id}, số lượng {qty}: hợp lệ");
    protected abstract decimal CalculatePrice(int qty);
    protected abstract void TakePayment(decimal amount);
    protected virtual void Ship(string id) => Console.WriteLine($"4. Giao hàng tiêu chuẩn cho {id}");
    protected virtual void AfterSales(string id) { }
}
public class RetailOrderProcessor : OrderProcessor
{
    protected override decimal CalculatePrice(int qty) { var p = qty * 100_000m; Console.WriteLine($"2. Giá bán lẻ: {p:N0}"); return p; }
    protected override void TakePayment(decimal a) => Console.WriteLine($"3. Thu {a:N0} ngay tại quầy/online");
}
public class WholesaleOrderProcessor : OrderProcessor
{
    protected override decimal CalculatePrice(int qty) { var p = qty * 100_000m * 0.8m; Console.WriteLine($"2. Giá sỉ (-20%): {p:N0}"); return p; }
    protected override void TakePayment(decimal a) => Console.WriteLine($"3. Ghi công nợ {a:N0} (30 ngày)");
    protected override void Ship(string id) => Console.WriteLine($"4. Giao hàng nguyên pallet cho đại lý {id}");
    protected override void AfterSales(string id) => Console.WriteLine($"5. Gửi bảng đối chiếu công nợ cho {id}");
}
