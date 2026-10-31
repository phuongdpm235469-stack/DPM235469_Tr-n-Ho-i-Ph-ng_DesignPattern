Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== MEDIATOR (mẫu chuẩn) ===");
var m = new ConcreteMediator();
m.A = new ComponentA(m); m.B = new ComponentB(m);
m.A.DoA();
m.B.DoB();

public interface IMediator { void Notify(object sender, string ev); }
public class ComponentA { private readonly IMediator _m; public ComponentA(IMediator m) => _m = m; public void DoA() { Console.WriteLine("A làm việc"); _m.Notify(this, "A"); } public void React() => Console.WriteLine("A phản ứng"); }
public class ComponentB { private readonly IMediator _m; public ComponentB(IMediator m) => _m = m; public void DoB() { Console.WriteLine("B làm việc"); _m.Notify(this, "B"); } public void React() => Console.WriteLine("B phản ứng"); }
public class ConcreteMediator : IMediator
{
    public ComponentA A; public ComponentB B;
    public void Notify(object sender, string ev) { if (ev == "A") B.React(); else if (ev == "B") A.React(); }
}
