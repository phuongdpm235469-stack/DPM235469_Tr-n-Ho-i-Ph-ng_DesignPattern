Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== STRATEGY: Chính sách giảm giá có thể thay đổi lúc chạy ===");
decimal subtotal = 2_000_000;
var checkout = new CheckoutCalculator(new NoDiscount());
Console.WriteLine($"Không giảm      : {checkout.Total(subtotal):N0}");

checkout.SetStrategy(new PercentDiscount(10));
Console.WriteLine($"Giảm 10%        : {checkout.Total(subtotal):N0}");

checkout.SetStrategy(new VipDiscount());
Console.WriteLine($"Khách VIP       : {checkout.Total(subtotal):N0}");

checkout.SetStrategy(new FixedAmountDiscount(150_000));
Console.WriteLine($"Voucher 150k    : {checkout.Total(subtotal):N0}");

public interface IDiscountStrategy { decimal Apply(decimal subtotal); }
public class NoDiscount : IDiscountStrategy { public decimal Apply(decimal s) => s; }
public class PercentDiscount : IDiscountStrategy
{
    private readonly decimal _p; public PercentDiscount(decimal p) => _p = p;
    public decimal Apply(decimal s) => s * (1 - _p / 100);
}
public class FixedAmountDiscount : IDiscountStrategy
{
    private readonly decimal _a; public FixedAmountDiscount(decimal a) => _a = a;
    public decimal Apply(decimal s) => Math.Max(0, s - _a);
}
public class VipDiscount : IDiscountStrategy
{
    // VIP: giảm 15%, tối đa 500k
    public decimal Apply(decimal s) => s - Math.Min(s * 0.15m, 500_000);
}
public class CheckoutCalculator
{
    private IDiscountStrategy _strategy;
    public CheckoutCalculator(IDiscountStrategy s) => _strategy = s;
    public void SetStrategy(IDiscountStrategy s) => _strategy = s;
    public decimal Total(decimal subtotal) => _strategy.Apply(subtotal);
}
