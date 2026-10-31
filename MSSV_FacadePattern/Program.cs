Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== FACADE (mẫu chuẩn) ===");
new Facade().Operation();

public class SubsystemA { public string Op1() => "A: sẵn sàng"; public string OpN() => "A: chạy!"; }
public class SubsystemB { public string Op1() => "B: sẵn sàng"; public string OpZ() => "B: chạy!"; }
public class Facade
{
    private readonly SubsystemA _a = new(); private readonly SubsystemB _b = new();
    public void Operation()
    {
        Console.WriteLine(_a.Op1()); Console.WriteLine(_b.Op1());
        Console.WriteLine(_a.OpN()); Console.WriteLine(_b.OpZ());
    }
}
