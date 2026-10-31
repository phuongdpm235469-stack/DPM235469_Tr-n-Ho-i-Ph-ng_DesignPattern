Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== PROXY (mẫu chuẩn - Protection Proxy) ===");
ISubject real = new RealSubject();
ISubject proxy = new Proxy(real, isAdmin: false);
proxy.Request();
proxy = new Proxy(real, isAdmin: true);
proxy.Request();

public interface ISubject { void Request(); }
public class RealSubject : ISubject { public void Request() => Console.WriteLine("RealSubject: xử lý yêu cầu."); }
public class Proxy : ISubject
{
    private readonly ISubject _real; private readonly bool _isAdmin;
    public Proxy(ISubject r, bool isAdmin) { _real = r; _isAdmin = isAdmin; }
    public void Request()
    {
        if (!_isAdmin) { Console.WriteLine("Proxy: TỪ CHỐI truy cập."); return; }
        Console.WriteLine("Proxy: kiểm tra quyền OK."); _real.Request();
    }
}
