Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== BUILDER: Khởi tạo đơn hàng ===");
var order = new OrderBuilder()
    .ForCustomer("Nguyễn Văn A")
    .AddItem("Áo sơ mi Oxford", 2, 350000)
    .AddItem("Cà vạt lụa", 1, 150000)
    .ApplyCoupon("GIAM20K", 20000)
    .WithExpressShipping(30000)
    .AddNote("Giao trong giờ hành chính")
    .Build();
Console.WriteLine(order);

public record OrderItem(string Name, int Quantity, decimal Price);

public sealed class Order
{
    public string Customer { get; init; }
    public IReadOnlyList<OrderItem> Items { get; init; }
    public string CouponCode { get; init; }
    public decimal Discount { get; init; }
    public decimal ShippingFee { get; init; }
    public string Note { get; init; }
    public decimal Total => Items.Sum(i => i.Price * i.Quantity) - Discount + ShippingFee;
    public override string ToString()
    {
        var lines = string.Join("\n", Items.Select(i => $"  - {i.Name} x{i.Quantity} = {i.Price * i.Quantity:N0}"));
        return $"Khách: {Customer}\n{lines}\n  Coupon: {CouponCode} (-{Discount:N0})\n  Ship: {ShippingFee:N0}\n  Ghi chú: {Note}\n  TỔNG: {Total:N0} VND";
    }
}

public class OrderBuilder
{
    private string _customer, _coupon, _note;
    private readonly List<OrderItem> _items = new();
    private decimal _discount, _ship;
    public OrderBuilder ForCustomer(string c) { _customer = c; return this; }
    public OrderBuilder AddItem(string name, int quantity, decimal price) { _items.Add(new OrderItem(name, quantity, price)); return this; }
    public OrderBuilder ApplyCoupon(string code, decimal amount) { _coupon = code; _discount = amount; return this; }
    public OrderBuilder WithExpressShipping(decimal fee) { _ship = fee; return this; }
    public OrderBuilder AddNote(string n) { _note = n; return this; }
    public Order Build()
    {
        if (string.IsNullOrEmpty(_customer)) throw new InvalidOperationException("Thiếu khách hàng");
        if (_items.Count == 0) throw new InvalidOperationException("Đơn hàng rỗng");
        return new Order { Customer = _customer, Items = _items.ToList(), CouponCode = _coupon, Discount = _discount, ShippingFee = _ship, Note = _note };
    }
}
