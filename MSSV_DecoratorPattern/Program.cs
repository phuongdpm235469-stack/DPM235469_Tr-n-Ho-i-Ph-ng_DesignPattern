Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== DECORATOR (mẫu chuẩn) ===");
IComponent c = new ConcreteComponent();
c = new DecoratorA(c);
c = new DecoratorB(c);
Console.WriteLine(c.Operation());

public interface IComponent { string Operation(); }
public class ConcreteComponent : IComponent { public string Operation() => "Lõi"; }
public abstract class Decorator : IComponent
{
    protected IComponent _inner;
    protected Decorator(IComponent c) => _inner = c;
    public virtual string Operation() => _inner.Operation();
}
public class DecoratorA : Decorator { public DecoratorA(IComponent c) : base(c) { } public override string Operation() => $"A({_inner.Operation()})"; }
public class DecoratorB : Decorator { public DecoratorB(IComponent c) : base(c) { } public override string Operation() => $"B({_inner.Operation()})"; }
