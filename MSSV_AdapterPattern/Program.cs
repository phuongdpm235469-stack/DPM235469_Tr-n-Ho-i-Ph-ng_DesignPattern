Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== ADAPTER (mẫu chuẩn) ===");
ITarget target = new Adapter(new Adaptee());
Console.WriteLine(target.GetRequest());

public interface ITarget { string GetRequest(); }
public class Adaptee { public string GetSpecificRequest() => "dữ liệu cũ"; }
public class Adapter : ITarget
{
    private readonly Adaptee _a;
    public Adapter(Adaptee a) => _a = a;
    public string GetRequest() => "Adapter: (đã chuyển đổi) " + _a.GetSpecificRequest().ToUpper();
}
