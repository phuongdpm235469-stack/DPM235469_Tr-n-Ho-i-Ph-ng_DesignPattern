Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== VISITOR (mẫu chuẩn) ===");
var elements = new List<IElement> { new ElementA(), new ElementB() };
foreach (var e in elements) e.Accept(new PrintVisitor());
foreach (var e in elements) e.Accept(new ExportVisitor());

public interface IVisitor { void Visit(ElementA a); void Visit(ElementB b); }
public interface IElement { void Accept(IVisitor v); }
public class ElementA : IElement { public string ExclusiveA() => "A"; public void Accept(IVisitor v) => v.Visit(this); }
public class ElementB : IElement { public string ExclusiveB() => "B"; public void Accept(IVisitor v) => v.Visit(this); }
public class PrintVisitor : IVisitor
{
    public void Visit(ElementA a) => Console.WriteLine("Print: " + a.ExclusiveA());
    public void Visit(ElementB b) => Console.WriteLine("Print: " + b.ExclusiveB());
}
public class ExportVisitor : IVisitor
{
    public void Visit(ElementA a) => Console.WriteLine("Export JSON A");
    public void Visit(ElementB b) => Console.WriteLine("Export JSON B");
}
