Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== INTERPRETER: Quy tắc áp dụng coupon ===");
// Quy tắc: (Tổng > 500.000 VÀ khách là VIP) HOẶC (Tổng > 2.000.000)
IRule rule = new OrRule(
    new AndRule(new TotalGreaterThan(500_000), new VipRule()),
    new TotalGreaterThan(2_000_000));

var cases = new[]
{
    new SalesContext { Total = 600_000, IsVip = true },
    new SalesContext { Total = 600_000, IsVip = false },
    new SalesContext { Total = 2_500_000, IsVip = false },
    new SalesContext { Total = 300_000, IsVip = true }
};
foreach (var c in cases)
    Console.WriteLine($"Đơn {c.Total,10:N0} | VIP={c.IsVip,-5} => {(rule.Interpret(c) ? "ĐƯỢC dùng coupon" : "KHÔNG đủ điều kiện")}");

public class SalesContext { public decimal Total; public bool IsVip; }
public interface IRule { bool Interpret(SalesContext c); }
public class TotalGreaterThan : IRule { private readonly decimal _v; public TotalGreaterThan(decimal v) => _v = v; public bool Interpret(SalesContext c) => c.Total > _v; }
public class VipRule : IRule { public bool Interpret(SalesContext c) => c.IsVip; }
public class AndRule : IRule { private readonly IRule _l, _r; public AndRule(IRule l, IRule r) { _l = l; _r = r; } public bool Interpret(SalesContext c) => _l.Interpret(c) && _r.Interpret(c); }
public class OrRule : IRule { private readonly IRule _l, _r; public OrRule(IRule l, IRule r) { _l = l; _r = r; } public bool Interpret(SalesContext c) => _l.Interpret(c) || _r.Interpret(c); }
public class NotRule : IRule { private readonly IRule _e; public NotRule(IRule e) => _e = e; public bool Interpret(SalesContext c) => !_e.Interpret(c); }
