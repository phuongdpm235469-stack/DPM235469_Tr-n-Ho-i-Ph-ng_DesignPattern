Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== STATE: Vòng đời trạng thái đơn hàng ===");
var order = new SalesOrder("HD-2001");
order.Pay();       // Mới -> Đã thanh toán
order.Ship();
order.Cancel();    // đã giao vận -> không hủy được
order.Deliver();
order.Pay();       // đã hoàn tất -> không hợp lệ

var order2 = new SalesOrder("HD-2002");
order2.Cancel();   // hủy khi còn Mới -> OK
order2.Ship();

public interface IOrderState
{
    string Name { get; }
    void Pay(SalesOrder o); void Ship(SalesOrder o); void Deliver(SalesOrder o); void Cancel(SalesOrder o);
}
public class SalesOrder
{
    public string Id { get; }
    private IOrderState _state = new NewState();
    public SalesOrder(string id) { Id = id; Console.WriteLine($"\nĐơn {id} tạo ở trạng thái [{_state.Name}]"); }
    public void SetState(IOrderState s) { Console.WriteLine($"   {Id}: [{_state.Name}] -> [{s.Name}]"); _state = s; }
    public void Pay() => _state.Pay(this);
    public void Ship() => _state.Ship(this);
    public void Deliver() => _state.Deliver(this);
    public void Cancel() => _state.Cancel(this);
}
public abstract class OrderStateBase : IOrderState
{
    public abstract string Name { get; }
    protected void Invalid(string action) => Console.WriteLine($"   ✗ Không thể '{action}' khi đơn ở trạng thái [{Name}]");
    public virtual void Pay(SalesOrder o) => Invalid("thanh toán");
    public virtual void Ship(SalesOrder o) => Invalid("giao vận");
    public virtual void Deliver(SalesOrder o) => Invalid("giao hàng");
    public virtual void Cancel(SalesOrder o) => Invalid("hủy");
}
public class NewState : OrderStateBase
{
    public override string Name => "Mới tạo";
    public override void Pay(SalesOrder o) => o.SetState(new PaidState());
    public override void Cancel(SalesOrder o) => o.SetState(new CancelledState());
}
public class PaidState : OrderStateBase
{
    public override string Name => "Đã thanh toán";
    public override void Ship(SalesOrder o) => o.SetState(new ShippedState());
    public override void Cancel(SalesOrder o) => o.SetState(new CancelledState());
}
public class ShippedState : OrderStateBase
{
    public override string Name => "Đang giao";
    public override void Deliver(SalesOrder o) => o.SetState(new DeliveredState());
}
public class DeliveredState : OrderStateBase { public override string Name => "Đã giao"; }
public class CancelledState : OrderStateBase { public override string Name => "Đã hủy"; }
