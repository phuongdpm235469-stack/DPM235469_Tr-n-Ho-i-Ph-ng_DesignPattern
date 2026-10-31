Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== TEMPLATE METHOD (mẫu chuẩn) ===");
new ConcreteA().TemplateMethod();
Console.WriteLine();
new ConcreteB().TemplateMethod();

public abstract class AbstractClass
{
    public void TemplateMethod()
    {
        Step1(); Step2(); Hook(); Step3();
    }
    protected void Step1() => Console.WriteLine("Bước 1 (cố định)");
    protected abstract void Step2();
    protected virtual void Hook() { }
    protected void Step3() => Console.WriteLine("Bước 3 (cố định)");
}
public class ConcreteA : AbstractClass { protected override void Step2() => Console.WriteLine("Bước 2 của A"); }
public class ConcreteB : AbstractClass
{
    protected override void Step2() => Console.WriteLine("Bước 2 của B");
    protected override void Hook() => Console.WriteLine("Hook của B");
}
