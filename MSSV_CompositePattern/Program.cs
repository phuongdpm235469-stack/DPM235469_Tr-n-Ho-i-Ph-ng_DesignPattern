Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== COMPOSITE (mẫu chuẩn) ===");
var root = new Composite("root");
var branch = new Composite("branch");
branch.Add(new Leaf("leaf-1"));
branch.Add(new Leaf("leaf-2"));
root.Add(branch);
root.Add(new Leaf("leaf-3"));
Console.WriteLine(root.Operation());

public abstract class Component { public abstract string Operation(); }
public class Leaf : Component
{
    private readonly string _name;
    public Leaf(string n) => _name = n;
    public override string Operation() => _name;
}
public class Composite : Component
{
    private readonly string _name;
    private readonly List<Component> _children = new();
    public Composite(string n) => _name = n;
    public void Add(Component c) => _children.Add(c);
    public override string Operation() => $"{_name}({string.Join("+", _children.Select(c => c.Operation()))})";
}
