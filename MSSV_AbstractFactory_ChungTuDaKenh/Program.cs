Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== ABSTRACT FACTORY: Chứng từ đa kênh ===");
IDocumentFactory[] channels = { new OfflinePosDocumentFactory(), new OnlineDocumentFactory() };
foreach (var factory in channels)
{
    Console.WriteLine($"--- {factory.GetType().Name} ---");
    Console.WriteLine(factory.CreateReceipt().Print("HD-1001", 1250000));
    Console.WriteLine(factory.CreateDeliveryNote().Print("HD-1001"));
}

public interface IReceiptDocument { string Print(string orderId, decimal total); }
public interface IDeliveryDocument { string Print(string orderId); }

public class ThermalReceipt : IReceiptDocument { public string Print(string id, decimal t) => $"Biên lai nhiệt K80 | {id} | {t:N0} VND"; }
public class WarehouseSlip : IDeliveryDocument { public string Print(string id) => $"Phiếu xuất kho vật lý | {id}"; }
public class EInvoicePdf : IReceiptDocument { public string Print(string id, decimal t) => $"Hóa đơn điện tử PDF gửi email | {id} | {t:N0} VND"; }
public class ShippingLabel : IDeliveryDocument { public string Print(string id) => $"Phiếu giao hàng có mã vạch cho shipper | {id}"; }

public interface IDocumentFactory { IReceiptDocument CreateReceipt(); IDeliveryDocument CreateDeliveryNote(); }
public class OfflinePosDocumentFactory : IDocumentFactory
{
    public IReceiptDocument CreateReceipt() => new ThermalReceipt();
    public IDeliveryDocument CreateDeliveryNote() => new WarehouseSlip();
}
public class OnlineDocumentFactory : IDocumentFactory
{
    public IReceiptDocument CreateReceipt() => new EInvoicePdf();
    public IDeliveryDocument CreateDeliveryNote() => new ShippingLabel();
}
