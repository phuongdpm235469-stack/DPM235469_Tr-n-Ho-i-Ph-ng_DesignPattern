Console.OutputEncoding = System.Text.Encoding.UTF8;

Console.WriteLine("=== BRIDGE: Tách nghiệp vụ đơn và thiết bị hiển thị ===");
IOrderRenderer[] devices = { new WebRenderer(), new MobileRenderer(), new PosTouchRenderer() };
foreach (var d in devices)
{
    new RetailOrder(d).Process();
    new WholesaleOrder(d).Process();
}
// 2 loại đơn x 3 thiết bị = 6 tổ hợp nhưng chỉ cần 2 + 3 = 5 lớp (không phải 6)

public interface IOrderRenderer { void RenderUI(string info); }
public class WebRenderer : IOrderRenderer { public void RenderUI(string i) => Console.WriteLine($"[WEB]    {i}"); }
public class MobileRenderer : IOrderRenderer { public void RenderUI(string i) => Console.WriteLine($"[MOBILE] {i}"); }
public class PosTouchRenderer : IOrderRenderer { public void RenderUI(string i) => Console.WriteLine($"[POS]    {i}"); }

public abstract class OrderLogic
{
    protected IOrderRenderer _renderer;   // Con trỏ cầu nối (Bridge)
    protected OrderLogic(IOrderRenderer r) => _renderer = r;
    public abstract void Process();
}
public class RetailOrder : OrderLogic
{
    public RetailOrder(IOrderRenderer r) : base(r) { }
    public override void Process() => _renderer.RenderUI("Đơn BÁN LẺ: giá niêm yết, thanh toán ngay.");
}
public class WholesaleOrder : OrderLogic
{
    public WholesaleOrder(IOrderRenderer r) : base(r) { }
    public override void Process() => _renderer.RenderUI("Đơn SỈ ĐẠI LÝ: chiết khấu theo số lượng, công nợ 30 ngày.");
}
