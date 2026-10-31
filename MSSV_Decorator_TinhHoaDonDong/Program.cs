Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== DECORATOR: Tính hóa đơn động ===");
IOrder order = new BaseOrder();                          // Trà sữa gốc 35.000
order = new ToppingDecorator(order, 10000);              // + trân châu
order = new VatDecorator(order, 0.08);                   // + VAT 8%
order = new ShippingDecorator(order, 15000);             // + ship
Console.WriteLine($"Mô tả : {order.Describe()}");
Console.WriteLine($"Tổng  : {order.GetCost():N0} VND");

public interface IOrder { double GetCost(); string Describe(); }
public class BaseOrder : IOrder
{
    public double GetCost() => 35000;
    public string Describe() => "Trà sữa";
}
public abstract class OrderDecorator : IOrder
{
    protected readonly IOrder _order;
    protected OrderDecorator(IOrder o) => _order = o;
    public abstract double GetCost();
    public abstract string Describe();
}
public class ToppingDecorator : OrderDecorator
{
    private readonly double _price;
    public ToppingDecorator(IOrder o, double price) : base(o) => _price = price;
    public override double GetCost() => _order.GetCost() + _price;
    public override string Describe() => _order.Describe() + " + Trân châu";
}
public class VatDecorator : OrderDecorator
{
    private readonly double _rate;
    public VatDecorator(IOrder o, double rate) : base(o) => _rate = rate;
    public override double GetCost() => _order.GetCost() * (1 + _rate);
    public override string Describe() => _order.Describe() + $" + VAT {_rate:P0}";
}
public class ShippingDecorator : OrderDecorator
{
    private readonly double _fee;
    public ShippingDecorator(IOrder o, double fee) : base(o) => _fee = fee;
    public override double GetCost() => _order.GetCost() + _fee;
    public override string Describe() => _order.Describe() + " + Ship";
}
