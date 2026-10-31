Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== OBSERVER: Cảnh báo tồn kho ===");
var product = new StockProduct("Laptop Dell XPS", 10);
product.Attach(new WarehouseObserver());
product.Attach(new PurchasingObserver());
product.Attach(new WebsiteObserver());

product.Sell(4);
product.Sell(4);   // còn 2 -> kích hoạt cảnh báo
product.Sell(2);   // hết hàng

public interface IStockObserver { void OnStockChanged(StockProduct p); }
public class StockProduct
{
    private readonly List<IStockObserver> _obs = new();
    public string Name { get; } public int Stock { get; private set; }
    public StockProduct(string name, int stock) { Name = name; Stock = stock; }
    public void Attach(IStockObserver o) => _obs.Add(o);
    public void Detach(IStockObserver o) => _obs.Remove(o);
    public void Sell(int qty)
    {
        Stock -= qty;
        Console.WriteLine($"\nBán {qty} {Name}, tồn kho còn {Stock}");
        foreach (var o in _obs) o.OnStockChanged(this);
    }
}
public class WarehouseObserver : IStockObserver
{
    public void OnStockChanged(StockProduct p) { if (p.Stock <= 3) Console.WriteLine($"   [Kho] Cảnh báo: {p.Name} sắp hết ({p.Stock})."); }
}
public class PurchasingObserver : IStockObserver
{
    public void OnStockChanged(StockProduct p) { if (p.Stock <= 3) Console.WriteLine($"   [Mua hàng] Tạo đề nghị nhập thêm {p.Name}."); }
}
public class WebsiteObserver : IStockObserver
{
    public void OnStockChanged(StockProduct p) { if (p.Stock == 0) Console.WriteLine($"   [Website] Chuyển {p.Name} sang 'Hết hàng'."); }
}
