Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== VISITOR: Tính thuế & phí theo loại hàng ===");
var cart = new List<IProductElement>
{
    new Food("Gạo ST25", 200_000),
    new Electronics("Tai nghe Bluetooth", 1_500_000),
    new Clothing("Áo khoác", 800_000)
};

var tax = new TaxVisitor();
var ship = new ShippingFeeVisitor();
foreach (var p in cart) { p.Accept(tax); p.Accept(ship); }
Console.WriteLine($"\nTổng thuế : {tax.Total:N0}");
Console.WriteLine($"Tổng phí ship: {ship.Total:N0}");

public interface IProductVisitor
{
    void Visit(Food f); void Visit(Electronics e); void Visit(Clothing c);
}
public interface IProductElement { void Accept(IProductVisitor v); }
public class Food : IProductElement
{
    public string Name { get; } public decimal Price { get; }
    public Food(string n, decimal p) { Name = n; Price = p; }
    public void Accept(IProductVisitor v) => v.Visit(this);
}
public class Electronics : IProductElement
{
    public string Name { get; } public decimal Price { get; }
    public Electronics(string n, decimal p) { Name = n; Price = p; }
    public void Accept(IProductVisitor v) => v.Visit(this);
}
public class Clothing : IProductElement
{
    public string Name { get; } public decimal Price { get; }
    public Clothing(string n, decimal p) { Name = n; Price = p; }
    public void Accept(IProductVisitor v) => v.Visit(this);
}
// Thêm phép toán mới chỉ cần thêm Visitor, không sửa các lớp sản phẩm
public class TaxVisitor : IProductVisitor
{
    public decimal Total { get; private set; }
    private void Add(string n, decimal t, decimal rate) { Total += t; Console.WriteLine($"[Thuế {rate:P0}] {n}: {t:N0}"); }
    public void Visit(Food f) => Add(f.Name, f.Price * 0.05m, 0.05m);
    public void Visit(Electronics e) => Add(e.Name, e.Price * 0.10m, 0.10m);
    public void Visit(Clothing c) => Add(c.Name, c.Price * 0.08m, 0.08m);
}
public class ShippingFeeVisitor : IProductVisitor
{
    public decimal Total { get; private set; }
    private void Add(string n, decimal fee) { Total += fee; Console.WriteLine($"[Ship] {n}: {fee:N0}"); }
    public void Visit(Food f) => Add(f.Name, 20_000);
    public void Visit(Electronics e) => Add(e.Name, 35_000);
    public void Visit(Clothing c) => Add(c.Name, 15_000);
}
