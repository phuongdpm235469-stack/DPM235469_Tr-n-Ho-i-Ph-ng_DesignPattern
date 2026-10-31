Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== CHAIN OF RESPONSIBILITY: Duyệt giảm giá nhiều cấp ===");
var staff = new StaffApprover();
var manager = new ManagerApprover();
var director = new DirectorApprover();
staff.SetNext(manager).SetNext(director);

foreach (var pct in new[] { 3, 12, 25, 40 })
    staff.Approve(new DiscountRequest { Customer = "Đại lý Phát Lộc", Percent = pct });

public class DiscountRequest { public string Customer; public int Percent; }

public abstract class Approver
{
    private Approver _next;
    protected abstract string Role { get; }
    protected abstract int MaxPercent { get; }
    public Approver SetNext(Approver n) { _next = n; return n; }
    public void Approve(DiscountRequest r)
    {
        if (r.Percent <= MaxPercent) Console.WriteLine($"Giảm {r.Percent}% cho {r.Customer}: {Role} DUYỆT.");
        else if (_next != null) { Console.WriteLine($"Giảm {r.Percent}%: {Role} không đủ thẩm quyền (tối đa {MaxPercent}%), chuyển cấp trên..."); _next.Approve(r); }
        else Console.WriteLine($"Giảm {r.Percent}% cho {r.Customer}: TỪ CHỐI (vượt mọi thẩm quyền).");
    }
}
public class StaffApprover : Approver { protected override string Role => "Nhân viên"; protected override int MaxPercent => 5; }
public class ManagerApprover : Approver { protected override string Role => "Quản lý"; protected override int MaxPercent => 15; }
public class DirectorApprover : Approver { protected override string Role => "Giám đốc"; protected override int MaxPercent => 30; }
