Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== ITERATOR (mẫu chuẩn) ===");
var col = new WordCollection();
col.Add("một"); col.Add("hai"); col.Add("ba");
Console.WriteLine("Thuận:");
for (var it = col.CreateIterator(); it.HasNext();) Console.WriteLine("  " + it.Next());
Console.WriteLine("Ngược:");
for (var it = col.CreateReverseIterator(); it.HasNext();) Console.WriteLine("  " + it.Next());

public interface IIterator<T> { bool HasNext(); T Next(); }
public class WordCollection
{
    private readonly List<string> _items = new();
    public void Add(string s) => _items.Add(s);
    public int Count => _items.Count;
    public string this[int i] => _items[i];
    public IIterator<string> CreateIterator() => new ForwardIterator(this);
    public IIterator<string> CreateReverseIterator() => new ReverseIterator(this);
}
public class ForwardIterator : IIterator<string>
{
    private readonly WordCollection _c; private int _i;
    public ForwardIterator(WordCollection c) => _c = c;
    public bool HasNext() => _i < _c.Count;
    public string Next() => _c[_i++];
}
public class ReverseIterator : IIterator<string>
{
    private readonly WordCollection _c; private int _i;
    public ReverseIterator(WordCollection c) { _c = c; _i = c.Count - 1; }
    public bool HasNext() => _i >= 0;
    public string Next() => _c[_i--];
}
