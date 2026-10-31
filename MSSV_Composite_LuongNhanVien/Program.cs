Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== COMPOSITE: Lương nhân viên theo cấu trúc cây ===");

var gd = new QuanLy("Trần Giám Đốc", 40_000_000);
var truongKho = new QuanLy("Lê Trưởng Kho", 20_000_000);
var truongBH = new QuanLy("Phạm Trưởng Bán Hàng", 22_000_000);

truongKho.Add(new NhanVienKho("Võ Thủ Kho", 9_000_000));
truongKho.Add(new NhanVienKho("Đỗ Bốc Xếp", 7_500_000));
truongBH.Add(new NhanVienBanHang("Nguyễn Thu Ngân", 8_000_000, 25_000_000));
truongBH.Add(new NhanVienBanHang("Huỳnh Tư Vấn", 8_500_000, 40_000_000));
gd.Add(truongKho);
gd.Add(truongBH);

gd.Print(0);
Console.WriteLine($"\nTỔNG QUỸ LƯƠNG TOÀN CÔNG TY: {gd.GetSalary():N0} VND");
Console.WriteLine($"Quỹ lương phòng bán hàng   : {truongBH.GetSalary():N0} VND");

public interface IEmployee
{
    string Name { get; }
    decimal GetSalary();
    void Print(int level);
}
// Leaf: nhân viên bán hàng = lương cơ bản + 2% doanh số
public class NhanVienBanHang : IEmployee
{
    private readonly decimal _base, _sales;
    public string Name { get; }
    public NhanVienBanHang(string name, decimal baseSalary, decimal sales) { Name = name; _base = baseSalary; _sales = sales; }
    public decimal GetSalary() => _base + _sales * 0.02m;
    public void Print(int level) => Console.WriteLine($"{new string(' ', level * 3)}- {Name} (BH): {GetSalary():N0}");
}
// Leaf: nhân viên kho = lương cơ bản + phụ cấp độc hại 500k
public class NhanVienKho : IEmployee
{
    private readonly decimal _base;
    public string Name { get; }
    public NhanVienKho(string name, decimal baseSalary) { Name = name; _base = baseSalary; }
    public decimal GetSalary() => _base + 500_000;
    public void Print(int level) => Console.WriteLine($"{new string(' ', level * 3)}- {Name} (Kho): {GetSalary():N0}");
}
// Composite: quản lý = lương của mình + lương cấp dưới
public class QuanLy : IEmployee
{
    private readonly decimal _base;
    private readonly List<IEmployee> _subs = new();
    public string Name { get; }
    public QuanLy(string name, decimal baseSalary) { Name = name; _base = baseSalary; }
    public void Add(IEmployee e) => _subs.Add(e);
    public decimal GetSalary() => _base + _subs.Sum(s => s.GetSalary());
    public void Print(int level)
    {
        Console.WriteLine($"{new string(' ', level * 3)}+ {Name} (Quản lý) - lương riêng {_base:N0}, cả nhóm {GetSalary():N0}");
        foreach (var s in _subs) s.Print(level + 1);
    }
}
