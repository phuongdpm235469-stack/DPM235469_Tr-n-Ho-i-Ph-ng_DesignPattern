Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== FLYWEIGHT (mẫu chuẩn) ===");
var factory = new TreeTypeFactory();
var forest = new List<Tree>();
var rnd = new Random(1);
for (int i = 0; i < 1000; i++)
    forest.Add(new Tree(rnd.Next(100), rnd.Next(100), factory.Get(i % 2 == 0 ? "Sồi" : "Thông", "Xanh")));
Console.WriteLine($"Số cây: {forest.Count}, số TreeType thực sự trong RAM: {factory.Count}");

public class TreeType
{
    public string Name, Color;   // Intrinsic (chia sẻ)
    public TreeType(string n, string c) { Name = n; Color = c; }
}
public class TreeTypeFactory
{
    private readonly Dictionary<string, TreeType> _cache = new();
    public int Count => _cache.Count;
    public TreeType Get(string n, string c)
    {
        var k = n + "|" + c;
        if (!_cache.TryGetValue(k, out var t)) _cache[k] = t = new TreeType(n, c);
        return t;
    }
}
public class Tree { public int X, Y; public TreeType Type; public Tree(int x, int y, TreeType t) { X = x; Y = y; Type = t; } }   // X,Y: Extrinsic
