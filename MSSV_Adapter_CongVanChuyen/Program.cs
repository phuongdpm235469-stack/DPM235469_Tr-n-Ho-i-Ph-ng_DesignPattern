Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== ADAPTER: Cổng vận chuyển ===");
IShippingService[] carriers = { new GhtkAdapter(), new ViettelPostAdapter(), new DhlAdapter() };
foreach (var c in carriers)
    Console.WriteLine(c.CreateDelivery("12 Lê Lợi, An Giang", 2.5));

public interface IShippingService { string CreateDelivery(string address, double weightKg); }

// --- API riêng biệt của từng hãng (Adaptee) ---
public class GhtkSdkApi { public string SendOrderRequest(string addr, int grams) => $"GHTK-{grams}g-{addr.GetHashCode() & 0xFFF}"; }
public class ViettelPostApi { public string CreateBill(string json) => "VTP-" + json.Length; }
public class DhlApi { public string BookShipment(string[] lines, decimal kg) => $"DHL-{lines.Length}L-{kg}kg"; }

// --- Adapter chuyển chuẩn nội bộ sang API từng hãng ---
public class GhtkAdapter : IShippingService
{
    private readonly GhtkSdkApi _api = new();
    public string CreateDelivery(string addr, double wt) => _api.SendOrderRequest(addr, (int)(wt * 1000));
}
public class ViettelPostAdapter : IShippingService
{
    private readonly ViettelPostApi _api = new();
    public string CreateDelivery(string addr, double wt) => _api.CreateBill($"{{\"address\":\"{addr}\",\"weight\":{wt}}}");
}
public class DhlAdapter : IShippingService
{
    private readonly DhlApi _api = new();
    public string CreateDelivery(string addr, double wt) => _api.BookShipment(addr.Split(','), (decimal)wt);
}
