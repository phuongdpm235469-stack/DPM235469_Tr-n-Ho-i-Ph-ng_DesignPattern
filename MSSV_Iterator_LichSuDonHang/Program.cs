Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== ITERATOR: Duyệt lịch sử đơn hàng ===");
var history = new OrderHistory();
history.Add(new OrderRecord("HD-1001", "An", 500000, true));
history.Add(new OrderRecord("HD-1002", "Bình", 1200000, false));
history.Add(new OrderRecord("HD-1003", "Chi", 300000, true));
history.Add(new OrderRecord("HD-1004", "Dũng", 900000, false));

Console.WriteLine("-- Đơn mới nhất trước --");
for (var it = history.NewestFirst(); it.HasNext();) Console.WriteLine("  " + it.Next());

Console.WriteLine("-- Chỉ các đơn CHƯA thanh toán --");
for (var it = history.UnpaidOnly(); it.HasNext();) Console.WriteLine("  " + it.Next());

public record OrderRecord(string Id, string Customer, decimal Total, bool Paid)
{
    public override string ToString() => $"{Id} | {Customer} | {Total:N0} | {(Paid ? "Đã TT" : "Chưa TT")}";
}
public interface IOrderIterator { bool HasNext(); OrderRecord Next(); }
public class OrderHistory
{
    private readonly List<OrderRecord> _list = new();
    public void Add(OrderRecord r) => _list.Add(r);
    public IOrderIterator NewestFirst() => new ListIterator(_list.AsEnumerable().Reverse().ToList());
    public IOrderIterator UnpaidOnly() => new ListIterator(_list.Where(o => !o.Paid).ToList());
}
public class ListIterator : IOrderIterator
{
    private readonly List<OrderRecord> _l; private int _i;
    public ListIterator(List<OrderRecord> l) => _l = l;
    public bool HasNext() => _i < _l.Count;
    public OrderRecord Next() => _l[_i++];
}
