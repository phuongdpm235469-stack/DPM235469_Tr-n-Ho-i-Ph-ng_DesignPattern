Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== FACTORY METHOD (mẫu chuẩn) ===");
foreach (Creator c in new Creator[] { new CreatorA(), new CreatorB() })
    Console.WriteLine(c.SomeOperation());

public interface IProduct { string Operation(); }
public class ProductA : IProduct { public string Operation() => "Kết quả của ProductA"; }
public class ProductB : IProduct { public string Operation() => "Kết quả của ProductB"; }
public abstract class Creator
{
    public abstract IProduct FactoryMethod();
    public string SomeOperation() => "Creator: " + FactoryMethod().Operation();
}
public class CreatorA : Creator { public override IProduct FactoryMethod() => new ProductA(); }
public class CreatorB : Creator { public override IProduct FactoryMethod() => new ProductB(); }
