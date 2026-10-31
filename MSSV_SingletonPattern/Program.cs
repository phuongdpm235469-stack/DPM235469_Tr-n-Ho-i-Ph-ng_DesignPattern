Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== SINGLETON (mẫu chuẩn) ===");
var a = AppConfig.Instance;
var b = AppConfig.Instance;
a.Set("Theme", "Dark");
Console.WriteLine($"Cùng một thể hiện? {ReferenceEquals(a, b)}");
Console.WriteLine($"b.Theme = {b.Get("Theme")}");

public sealed class AppConfig
{
    private static readonly Lazy<AppConfig> _instance = new(() => new AppConfig());
    private readonly Dictionary<string, string> _data = new();
    private AppConfig() { }
    public static AppConfig Instance => _instance.Value;
    public void Set(string k, string v) => _data[k] = v;
    public string Get(string k) => _data.TryGetValue(k, out var v) ? v : null;
}
