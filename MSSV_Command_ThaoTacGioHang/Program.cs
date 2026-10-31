Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== COMMAND: Thao tác giỏ hàng có Undo ===");
var cart = new ShoppingCart();
var mgr = new CartCommandManager();

mgr.Run(new AddItemCommand(cart, "Áo thun", 2, 150000));
mgr.Run(new AddItemCommand(cart, "Quần jean", 1, 400000));
mgr.Run(new RemoveItemCommand(cart, "Áo thun"));
cart.Print();

Console.WriteLine("\n-- Hoàn tác 2 thao tác --");
mgr.Undo(); mgr.Undo();
cart.Print();

public class ShoppingCart
{
    public Dictionary<string, (int Qty, decimal Price)> Items { get; } = new();
    public void Print() => Console.WriteLine("Giỏ: " + (Items.Count == 0 ? "(trống)" : string.Join("; ", Items.Select(i => $"{i.Key} x{i.Value.Qty}"))) + $" | Tổng {Items.Sum(i => i.Value.Qty * i.Value.Price):N0}");
}
public interface ICartCommand { void Execute(); void Undo(); }
public class AddItemCommand : ICartCommand
{
    private readonly ShoppingCart _c; private readonly string _n; private readonly int _q; private readonly decimal _p;
    public AddItemCommand(ShoppingCart c, string n, int q, decimal p) { _c = c; _n = n; _q = q; _p = p; }
    public void Execute() { _c.Items[_n] = (_q, _p); Console.WriteLine($"+ Thêm {_n}"); }
    public void Undo() { _c.Items.Remove(_n); Console.WriteLine($"~ Hoàn tác thêm {_n}"); }
}
public class RemoveItemCommand : ICartCommand
{
    private readonly ShoppingCart _c; private readonly string _n; private (int Qty, decimal Price) _backup;
    public RemoveItemCommand(ShoppingCart c, string n) { _c = c; _n = n; }
    public void Execute() { _backup = _c.Items[_n]; _c.Items.Remove(_n); Console.WriteLine($"- Xóa {_n}"); }
    public void Undo() { _c.Items[_n] = _backup; Console.WriteLine($"~ Hoàn tác xóa {_n}"); }
}
public class CartCommandManager
{
    private readonly Stack<ICartCommand> _history = new();
    public void Run(ICartCommand c) { c.Execute(); _history.Push(c); }
    public void Undo() { if (_history.Count > 0) _history.Pop().Undo(); }
}
