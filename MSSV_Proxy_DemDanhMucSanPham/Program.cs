Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== PROXY: Bộ nhớ đệm danh mục sản phẩm ===");
var real = new RealProductService();
IProductService service = new ProductServiceProxy(real, new InMemoryCache());

for (int i = 1; i <= 3; i++)
{
    var p = service.GetById(101);
    Console.WriteLine($"Lần {i}: {p.Name} - {p.Price:N0}");
}
service.GetById(102);
Console.WriteLine($"\nTổng số lần chạm CSDL thật: {real.DbHits} (thay vì 4)");

public class Product { public int Id; public string Name; public decimal Price; }
public interface IProductService { Product GetById(int id); }

public class RealProductService : IProductService
{
    public int DbHits { get; private set; }
    public Product GetById(int id)
    {
        DbHits++;
        Console.WriteLine($"   [SQL] SELECT * FROM Products WHERE Id={id}");
        Thread.Sleep(100);   // mô phỏng truy vấn chậm
        return new Product { Id = id, Name = $"Sản phẩm #{id}", Price = 150000 + id };
    }
}
public interface ICache { T Get<T>(string key) where T : class; void Set<T>(string key, T v, TimeSpan ttl) where T : class; }
public class InMemoryCache : ICache
{
    private readonly Dictionary<string, (object v, DateTime exp)> _d = new();
    public T Get<T>(string key) where T : class => _d.TryGetValue(key, out var e) && e.exp > DateTime.Now ? e.v as T : null;
    public void Set<T>(string key, T v, TimeSpan ttl) where T : class => _d[key] = (v, DateTime.Now + ttl);
}
public class ProductServiceProxy : IProductService
{
    private readonly RealProductService _real; private readonly ICache _cache;
    public ProductServiceProxy(RealProductService r, ICache c) { _real = r; _cache = c; }
    public Product GetById(int id)
    {
        var cached = _cache.Get<Product>($"prod:{id}");
        if (cached != null) { Console.WriteLine("   [Cache HIT]"); return cached; }
        var data = _real.GetById(id);                       // Cache miss -> đọc SQL
        _cache.Set($"prod:{id}", data, TimeSpan.FromMinutes(30));
        return data;
    }
}
