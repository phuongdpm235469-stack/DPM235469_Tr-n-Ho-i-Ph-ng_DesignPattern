Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== STRATEGY (mẫu chuẩn) ===");
var calc = new Calculator(new Add());
Console.WriteLine($"f(10, 5) = {calc.Run(10, 5)}");
calc.SetStrategy(new Multiply());
Console.WriteLine($"f(10, 5) = {calc.Run(10, 5)}");

public interface IStrategy { int Execute(int a, int b); }
public class Add : IStrategy { public int Execute(int a, int b) => a + b; }
public class Multiply : IStrategy { public int Execute(int a, int b) => a * b; }
public class Calculator
{
    private IStrategy _s;
    public Calculator(IStrategy s) => _s = s;
    public void SetStrategy(IStrategy s) => _s = s;
    public int Run(int a, int b) => _s.Execute(a, b);
}
