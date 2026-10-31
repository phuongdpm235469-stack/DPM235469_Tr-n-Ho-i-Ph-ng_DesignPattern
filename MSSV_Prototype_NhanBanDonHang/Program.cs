Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== PROTOTYPE: Re-order (nhân bản đơn hàng) ===");
var original = new Order { OrderId = InvoiceGenerator.Next(), Customer = "Đại lý Minh Tâm" };
original.Items.Add(new OrderItem { Name = "Gạo ST25 (bao 25kg)", Quantity = 40, Price = 520000 });
original.Items.Add(new OrderItem { Name = "Dầu ăn (thùng 6 chai)", Quantity = 15, Price = 310000 });

var reorder = original.DeepClone();
reorder.Items[0].Quantity = 60;   // sửa bản sao, KHÔNG ảnh hưởng đơn gốc

original.Print();
reorder.Print();

public static class InvoiceGenerator
{
    private static int _n = 1000;
    public static string Next() => $"HD-{++_n}";
}
public class OrderItem
{
    public string Name { get; set; }
    public int Quantity { get; set; }
    public decimal Price { get; set; }
    public OrderItem Clone() => (OrderItem)MemberwiseClone();
}
public class Order : ICloneable
{
    public string OrderId { get; set; }
    public string Customer { get; set; }
    public List<OrderItem> Items { get; set; } = new();
    public Order DeepClone()
    {
        var c = (Order)MemberwiseClone();
        c.Items = Items.Select(i => i.Clone()).ToList();   // Deep copy
        c.OrderId = InvoiceGenerator.Next();                // mã đơn mới
        return c;
    }
    object ICloneable.Clone() => DeepClone();
    public void Print()
    {
        Console.WriteLine($"[{OrderId}] {Customer} - Tổng: {Items.Sum(i => i.Quantity * i.Price):N0} VND");
        foreach (var i in Items) Console.WriteLine($"    {i.Name} x{i.Quantity}");
    }
}
