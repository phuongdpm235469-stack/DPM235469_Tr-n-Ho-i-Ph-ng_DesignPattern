Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== CHAIN OF RESPONSIBILITY (mẫu chuẩn) ===");
var a = new ConcreteHandler("A", 10);
var b = new ConcreteHandler("B", 20);
var c = new ConcreteHandler("C", 30);
a.SetNext(b).SetNext(c);
foreach (var v in new[] { 5, 18, 29, 50 }) a.Handle(v);

public abstract class Handler
{
    private Handler _next;
    public Handler SetNext(Handler n) { _next = n; return n; }
    public virtual void Handle(int request)
    {
        if (_next != null) _next.Handle(request);
        else Console.WriteLine($"Yêu cầu {request}: không ai xử lý được.");
    }
}
public class ConcreteHandler : Handler
{
    private readonly string _name; private readonly int _limit;
    public ConcreteHandler(string n, int limit) { _name = n; _limit = limit; }
    public override void Handle(int r)
    {
        if (r <= _limit) Console.WriteLine($"Yêu cầu {r}: {_name} xử lý.");
        else base.Handle(r);
    }
}
