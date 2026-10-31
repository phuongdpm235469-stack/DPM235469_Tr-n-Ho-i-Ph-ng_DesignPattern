Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== MEMENTO: Hoàn tác giỏ hàng bằng snapshot ===");
var cart = new Cart();
var history = new CartHistory();

cart.Add("Áo thun", 150000); history.Save(cart.CreateSnapshot());
cart.Add("Quần jean", 400000); history.Save(cart.CreateSnapshot());
cart.Add("Giày thể thao", 900000);
cart.Print("Hiện tại");

cart.Restore(history.Pop()); cart.Print("Sau hoàn tác 1");
cart.Restore(history.Pop()); cart.Print("Sau hoàn tác 2");

public class CartSnapshot
{
    public IReadOnlyDictionary<string, decimal> Items { get; }
    public CartSnapshot(Dictionary<string, decimal> items) => Items = new Dictionary<string, decimal>(items);
}
public class Cart
{
    private Dictionary<string, decimal> _items = new();
    public void Add(string name, decimal price) => _items[name] = price;
    public CartSnapshot CreateSnapshot() => new CartSnapshot(_items);
    public void Restore(CartSnapshot s) => _items = new Dictionary<string, decimal>(s.Items);
    public void Print(string label) => Console.WriteLine($"[{label}] {string.Join(", ", _items.Keys)} | Tổng: {_items.Values.Sum():N0}");
}
public class CartHistory
{
    private readonly Stack<CartSnapshot> _stack = new();
    public void Save(CartSnapshot s) => _stack.Push(s);
    public CartSnapshot Pop() => _stack.Pop();
}
