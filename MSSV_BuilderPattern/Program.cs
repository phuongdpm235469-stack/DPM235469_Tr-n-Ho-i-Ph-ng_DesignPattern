Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== BUILDER (mẫu chuẩn) ===");
var house = new HouseBuilder().SetWalls("Gạch").SetRoof("Ngói").SetGarage(true).Build();
Console.WriteLine(house);

public class House
{
    public string Walls, Roof;
    public bool Garage;
    public override string ToString() => $"Nhà: tường {Walls}, mái {Roof}, gara={Garage}";
}
public class HouseBuilder
{
    private readonly House _h = new();
    public HouseBuilder SetWalls(string w) { _h.Walls = w; return this; }
    public HouseBuilder SetRoof(string r) { _h.Roof = r; return this; }
    public HouseBuilder SetGarage(bool g) { _h.Garage = g; return this; }
    public House Build() => _h;
}
