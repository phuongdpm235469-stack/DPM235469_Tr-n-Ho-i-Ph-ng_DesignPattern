Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== FLYWEIGHT: Tối ưu bộ nhớ thông số sản phẩm ===");
var factory = new ProductSpecificationFactory();
var orderItems = new List<OrderItem>();
var rnd = new Random(7);
string[] models = { "iPhone 16 128GB", "iPhone 16 256GB", "iPhone 16 Pro 256GB" };

for (int i = 0; i < 100_000; i++)
{
    var spec = factory.Get(models[i % 3]);   // dùng chung
    orderItems.Add(new OrderItem { SerialNumber = $"IMEI{i:D8}", SoldPrice = 20_000_000 + rnd.Next(0, 3_000_000), Spec = spec });
}

Console.WriteLine($"Số dòng đơn hàng      : {orderItems.Count:N0}");
Console.WriteLine($"Số ProductSpecification thực tế trong RAM: {factory.Count}");
Console.WriteLine($"Ví dụ: {orderItems[0].SerialNumber} -> {orderItems[0].Spec.ModelName} ({orderItems[0].Spec.TechnicalSpecs})");
Console.WriteLine($"Cùng model dùng chung 1 đối tượng? {ReferenceEquals(orderItems[0].Spec, orderItems[3].Spec)}");

// Intrinsic: dùng chung
public class ProductSpecification
{
    public string ModelName { get; }
    public string TechnicalSpecs { get; }
    public byte[] ImageBytes { get; }
    public ProductSpecification(string model) { ModelName = model; TechnicalSpecs = "Chip A18, OLED 6.1\", " + model; ImageBytes = new byte[1024 * 100]; }
}
public class ProductSpecificationFactory
{
    private readonly Dictionary<string, ProductSpecification> _pool = new();
    public int Count => _pool.Count;
    public ProductSpecification Get(string model)
    {
        if (!_pool.TryGetValue(model, out var s)) _pool[model] = s = new ProductSpecification(model);
        return s;
    }
}
// Extrinsic: riêng từng giao dịch
public class OrderItem
{
    public string SerialNumber { get; set; }
    public decimal SoldPrice { get; set; }
    public ProductSpecification Spec { get; set; }
}
