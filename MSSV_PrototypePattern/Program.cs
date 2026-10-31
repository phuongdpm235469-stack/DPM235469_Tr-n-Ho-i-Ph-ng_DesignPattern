Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== PROTOTYPE (mẫu chuẩn) ===");
var s1 = new Shape { Color = "Đỏ" };
s1.Points.AddRange(new[] { 1, 2, 3 });
var s2 = s1.Clone();
s2.Color = "Xanh";
s2.Points.Add(99);
Console.WriteLine($"s1: {s1.Color} [{string.Join(",", s1.Points)}]");
Console.WriteLine($"s2: {s2.Color} [{string.Join(",", s2.Points)}]");

public interface IPrototype<T> { T Clone(); }
public class Shape : IPrototype<Shape>
{
    public string Color;
    public List<int> Points = new();
    public Shape Clone()
    {
        var c = (Shape)MemberwiseClone();   // shallow
        c.Points = new List<int>(Points);   // deep cho danh sách
        return c;
    }
}
