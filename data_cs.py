H = "Console.OutputEncoding = System.Text.Encoding.UTF8;\n"

# Mỗi phần tử: (category, tên mẫu, tên project Real, code Pattern, code Real)
ITEMS = []

# ============================== CREATIONAL ==============================
ITEMS.append(("Creational", "Singleton", "QuanLyPhienPOS", H + r'''
Console.WriteLine("=== SINGLETON (mẫu chuẩn) ===");
var a = AppConfig.Instance;
var b = AppConfig.Instance;
a.Set("Theme", "Dark");
Console.WriteLine($"Cùng một thể hiện? {ReferenceEquals(a, b)}");
Console.WriteLine($"b.Theme = {b.Get("Theme")}");

public sealed class AppConfig
{
    private static readonly Lazy<AppConfig> _instance = new(() => new AppConfig());
    private readonly Dictionary<string, string> _data = new();
    private AppConfig() { }
    public static AppConfig Instance => _instance.Value;
    public void Set(string k, string v) => _data[k] = v;
    public string Get(string k) => _data.TryGetValue(k, out var v) ? v : null;
}
''', H + r'''
Console.WriteLine("=== SINGLETON: Quản lý phiên POS ===");
Parallel.For(0, 5, i =>
{
    var no = PosSessionManager.Instance.NextInvoiceNo();
    Console.WriteLine($"Quầy thu ngân #{i} nhận số hóa đơn: {no}");
});
Console.WriteLine($"Tổng số hóa đơn đã cấp: {PosSessionManager.Instance.Issued}");

public sealed class PosSessionManager
{
    private static readonly Lazy<PosSessionManager> _instance = new(() => new PosSessionManager());
    private int _invoiceCounter = 1000;
    private PosSessionManager() { }
    public static PosSessionManager Instance => _instance.Value;
    public int Issued => _invoiceCounter - 1000;
    // Interlocked đảm bảo không trùng số hóa đơn khi nhiều quầy cùng thanh toán
    public string NextInvoiceNo() => $"HD-{Interlocked.Increment(ref _invoiceCounter)}";
}
'''))

ITEMS.append(("Creational", "Builder", "KhoiTaoDonHang", H + r'''
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
''', H + r'''
Console.WriteLine("=== BUILDER: Khởi tạo đơn hàng ===");
var order = new OrderBuilder()
    .ForCustomer("Nguyễn Văn A")
    .AddItem("Áo sơ mi Oxford", 2, 350000)
    .AddItem("Cà vạt lụa", 1, 150000)
    .ApplyCoupon("GIAM20K", 20000)
    .WithExpressShipping(30000)
    .AddNote("Giao trong giờ hành chính")
    .Build();
Console.WriteLine(order);

public record OrderItem(string Name, int Quantity, decimal Price);

public sealed class Order
{
    public string Customer { get; init; }
    public IReadOnlyList<OrderItem> Items { get; init; }
    public string CouponCode { get; init; }
    public decimal Discount { get; init; }
    public decimal ShippingFee { get; init; }
    public string Note { get; init; }
    public decimal Total => Items.Sum(i => i.Price * i.Quantity) - Discount + ShippingFee;
    public override string ToString()
    {
        var lines = string.Join("\n", Items.Select(i => $"  - {i.Name} x{i.Quantity} = {i.Price * i.Quantity:N0}"));
        return $"Khách: {Customer}\n{lines}\n  Coupon: {CouponCode} (-{Discount:N0})\n  Ship: {ShippingFee:N0}\n  Ghi chú: {Note}\n  TỔNG: {Total:N0} VND";
    }
}

public class OrderBuilder
{
    private string _customer, _coupon, _note;
    private readonly List<OrderItem> _items = new();
    private decimal _discount, _ship;
    public OrderBuilder ForCustomer(string c) { _customer = c; return this; }
    public OrderBuilder AddItem(string name, int quantity, decimal price) { _items.Add(new OrderItem(name, quantity, price)); return this; }
    public OrderBuilder ApplyCoupon(string code, decimal amount) { _coupon = code; _discount = amount; return this; }
    public OrderBuilder WithExpressShipping(decimal fee) { _ship = fee; return this; }
    public OrderBuilder AddNote(string n) { _note = n; return this; }
    public Order Build()
    {
        if (string.IsNullOrEmpty(_customer)) throw new InvalidOperationException("Thiếu khách hàng");
        if (_items.Count == 0) throw new InvalidOperationException("Đơn hàng rỗng");
        return new Order { Customer = _customer, Items = _items.ToList(), CouponCode = _coupon, Discount = _discount, ShippingFee = _ship, Note = _note };
    }
}
'''))

ITEMS.append(("Creational", "Prototype", "NhanBanDonHang", H + r'''
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
''', H + r'''
Console.WriteLine("=== PROTOTYPE: Re-order (nhân bản đơn hàng) ===");
var original = new Order { OrderId = InvoiceGenerator.Next(), Customer = "Đại lý Minh Tâm" };
original.Items.Add(new OrderItem { Name = "Gạo ST25 (bao 25kg)", Quantity = 40, Price = 520000 });
original.Items.Add(new OrderItem { Name = "Dầu ăn (thùng 6 chai)", Quantity = 15, Price = 310000 });

var reorder = original.DeepClone();
reorder.Items[0].Quantity = 60;   // sửa bản sao, KHÔNG ảnh hưởng đơn gốc

original.Print();
reorder.Print();

public static class InvoiceGenerator
{
    private static int _n = 1000;
    public static string Next() => $"HD-{++_n}";
}
public class OrderItem
{
    public string Name { get; set; }
    public int Quantity { get; set; }
    public decimal Price { get; set; }
    public OrderItem Clone() => (OrderItem)MemberwiseClone();
}
public class Order : ICloneable
{
    public string OrderId { get; set; }
    public string Customer { get; set; }
    public List<OrderItem> Items { get; set; } = new();
    public Order DeepClone()
    {
        var c = (Order)MemberwiseClone();
        c.Items = Items.Select(i => i.Clone()).ToList();   // Deep copy
        c.OrderId = InvoiceGenerator.Next();                // mã đơn mới
        return c;
    }
    object ICloneable.Clone() => DeepClone();
    public void Print()
    {
        Console.WriteLine($"[{OrderId}] {Customer} - Tổng: {Items.Sum(i => i.Quantity * i.Price):N0} VND");
        foreach (var i in Items) Console.WriteLine($"    {i.Name} x{i.Quantity}");
    }
}
'''))

ITEMS.append(("Creational", "FactoryMethod", "CongThanhToan", H + r'''
Console.WriteLine("=== FACTORY METHOD (mẫu chuẩn) ===");
foreach (Creator c in new Creator[] { new CreatorA(), new CreatorB() })
    Console.WriteLine(c.SomeOperation());

public interface IProduct { string Operation(); }
public class ProductA : IProduct { public string Operation() => "Kết quả của ProductA"; }
public class ProductB : IProduct { public string Operation() => "Kết quả của ProductB"; }
public abstract class Creator
{
    public abstract IProduct FactoryMethod();
    public string SomeOperation() => "Creator: " + FactoryMethod().Operation();
}
public class CreatorA : Creator { public override IProduct FactoryMethod() => new ProductA(); }
public class CreatorB : Creator { public override IProduct FactoryMethod() => new ProductB(); }
''', H + r'''
Console.WriteLine("=== FACTORY METHOD: Cổng thanh toán ===");
decimal total = 1250000;
PaymentProcessorFactory[] factories = { new CashFactory(), new MomoFactory(), new VisaFactory() };
foreach (var f in factories)
{
    IPaymentProcessor p = f.CreateProcessor();
    p.Process(total);
}
// Thêm ZaloPay chỉ cần thêm 1 lớp mới (OCP) - không sửa code cũ

public interface IPaymentProcessor { void Process(decimal amount); }
public class CashPayment : IPaymentProcessor { public void Process(decimal a) => Console.WriteLine($"[Tiền mặt] Thu {a:N0} VND tại quầy."); }
public class MomoPayment : IPaymentProcessor { public void Process(decimal a) => Console.WriteLine($"[MoMo] Gửi yêu cầu QR {a:N0} VND."); }
public class VisaPayment : IPaymentProcessor { public void Process(decimal a) => Console.WriteLine($"[Visa/Mastercard] Cà thẻ {a:N0} VND."); }

public abstract class PaymentProcessorFactory { public abstract IPaymentProcessor CreateProcessor(); }
public class CashFactory : PaymentProcessorFactory { public override IPaymentProcessor CreateProcessor() => new CashPayment(); }
public class MomoFactory : PaymentProcessorFactory { public override IPaymentProcessor CreateProcessor() => new MomoPayment(); }
public class VisaFactory : PaymentProcessorFactory { public override IPaymentProcessor CreateProcessor() => new VisaPayment(); }
'''))

ITEMS.append(("Creational", "AbstractFactory", "ChungTuDaKenh", H + r'''
Console.WriteLine("=== ABSTRACT FACTORY (mẫu chuẩn) ===");
foreach (IGuiFactory f in new IGuiFactory[] { new WinFactory(), new MacFactory() })
{
    Console.WriteLine(f.CreateButton().Render());
    Console.WriteLine(f.CreateCheckbox().Render());
}

public interface IButton { string Render(); }
public interface ICheckbox { string Render(); }
public interface IGuiFactory { IButton CreateButton(); ICheckbox CreateCheckbox(); }
public class WinButton : IButton { public string Render() => "[Windows Button]"; }
public class WinCheckbox : ICheckbox { public string Render() => "[Windows Checkbox]"; }
public class MacButton : IButton { public string Render() => "(Mac Button)"; }
public class MacCheckbox : ICheckbox { public string Render() => "(Mac Checkbox)"; }
public class WinFactory : IGuiFactory { public IButton CreateButton() => new WinButton(); public ICheckbox CreateCheckbox() => new WinCheckbox(); }
public class MacFactory : IGuiFactory { public IButton CreateButton() => new MacButton(); public ICheckbox CreateCheckbox() => new MacCheckbox(); }
''', H + r'''
Console.WriteLine("=== ABSTRACT FACTORY: Chứng từ đa kênh ===");
IDocumentFactory[] channels = { new OfflinePosDocumentFactory(), new OnlineDocumentFactory() };
foreach (var factory in channels)
{
    Console.WriteLine($"--- {factory.GetType().Name} ---");
    Console.WriteLine(factory.CreateReceipt().Print("HD-1001", 1250000));
    Console.WriteLine(factory.CreateDeliveryNote().Print("HD-1001"));
}

public interface IReceiptDocument { string Print(string orderId, decimal total); }
public interface IDeliveryDocument { string Print(string orderId); }

public class ThermalReceipt : IReceiptDocument { public string Print(string id, decimal t) => $"Biên lai nhiệt K80 | {id} | {t:N0} VND"; }
public class WarehouseSlip : IDeliveryDocument { public string Print(string id) => $"Phiếu xuất kho vật lý | {id}"; }
public class EInvoicePdf : IReceiptDocument { public string Print(string id, decimal t) => $"Hóa đơn điện tử PDF gửi email | {id} | {t:N0} VND"; }
public class ShippingLabel : IDeliveryDocument { public string Print(string id) => $"Phiếu giao hàng có mã vạch cho shipper | {id}"; }

public interface IDocumentFactory { IReceiptDocument CreateReceipt(); IDeliveryDocument CreateDeliveryNote(); }
public class OfflinePosDocumentFactory : IDocumentFactory
{
    public IReceiptDocument CreateReceipt() => new ThermalReceipt();
    public IDeliveryDocument CreateDeliveryNote() => new WarehouseSlip();
}
public class OnlineDocumentFactory : IDocumentFactory
{
    public IReceiptDocument CreateReceipt() => new EInvoicePdf();
    public IDeliveryDocument CreateDeliveryNote() => new ShippingLabel();
}
'''))

# ============================== STRUCTURAL ==============================
ITEMS.append(("Structural", "Adapter", "CongVanChuyen", H + r'''
Console.WriteLine("=== ADAPTER (mẫu chuẩn) ===");
ITarget target = new Adapter(new Adaptee());
Console.WriteLine(target.GetRequest());

public interface ITarget { string GetRequest(); }
public class Adaptee { public string GetSpecificRequest() => "dữ liệu cũ"; }
public class Adapter : ITarget
{
    private readonly Adaptee _a;
    public Adapter(Adaptee a) => _a = a;
    public string GetRequest() => "Adapter: (đã chuyển đổi) " + _a.GetSpecificRequest().ToUpper();
}
''', H + r'''
Console.WriteLine("=== ADAPTER: Cổng vận chuyển ===");
IShippingService[] carriers = { new GhtkAdapter(), new ViettelPostAdapter(), new DhlAdapter() };
foreach (var c in carriers)
    Console.WriteLine(c.CreateDelivery("12 Lê Lợi, An Giang", 2.5));

public interface IShippingService { string CreateDelivery(string address, double weightKg); }

// --- API riêng biệt của từng hãng (Adaptee) ---
public class GhtkSdkApi { public string SendOrderRequest(string addr, int grams) => $"GHTK-{grams}g-{addr.GetHashCode() & 0xFFF}"; }
public class ViettelPostApi { public string CreateBill(string json) => "VTP-" + json.Length; }
public class DhlApi { public string BookShipment(string[] lines, decimal kg) => $"DHL-{lines.Length}L-{kg}kg"; }

// --- Adapter chuyển chuẩn nội bộ sang API từng hãng ---
public class GhtkAdapter : IShippingService
{
    private readonly GhtkSdkApi _api = new();
    public string CreateDelivery(string addr, double wt) => _api.SendOrderRequest(addr, (int)(wt * 1000));
}
public class ViettelPostAdapter : IShippingService
{
    private readonly ViettelPostApi _api = new();
    public string CreateDelivery(string addr, double wt) => _api.CreateBill($"{{\"address\":\"{addr}\",\"weight\":{wt}}}");
}
public class DhlAdapter : IShippingService
{
    private readonly DhlApi _api = new();
    public string CreateDelivery(string addr, double wt) => _api.BookShipment(addr.Split(','), (decimal)wt);
}
'''))

ITEMS.append(("Structural", "Bridge", "NenTangThietBi", H + r'''
Console.WriteLine("=== BRIDGE (mẫu chuẩn) ===");
var tv = new RemoteControl(new Tv());
var radio = new AdvancedRemote(new Radio());
tv.TogglePower();
radio.TogglePower();
radio.Mute();

public interface IDevice { void SetPower(bool on); void SetVolume(int v); }
public class Tv : IDevice { public void SetPower(bool on) => Console.WriteLine($"TV {(on ? "bật" : "tắt")}"); public void SetVolume(int v) => Console.WriteLine($"TV volume={v}"); }
public class Radio : IDevice { public void SetPower(bool on) => Console.WriteLine($"Radio {(on ? "bật" : "tắt")}"); public void SetVolume(int v) => Console.WriteLine($"Radio volume={v}"); }
public class RemoteControl
{
    protected IDevice _device; private bool _on;
    public RemoteControl(IDevice d) => _device = d;
    public void TogglePower() { _on = !_on; _device.SetPower(_on); }
}
public class AdvancedRemote : RemoteControl
{
    public AdvancedRemote(IDevice d) : base(d) { }
    public void Mute() => _device.SetVolume(0);
}
''', H + r'''
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
'''))

ITEMS.append(("Structural", "Composite", "LuongNhanVien", H + r'''
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
''', H + r'''
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
'''))

ITEMS.append(("Structural", "Decorator", "TinhHoaDonDong", H + r'''
Console.WriteLine("=== DECORATOR (mẫu chuẩn) ===");
IComponent c = new ConcreteComponent();
c = new DecoratorA(c);
c = new DecoratorB(c);
Console.WriteLine(c.Operation());

public interface IComponent { string Operation(); }
public class ConcreteComponent : IComponent { public string Operation() => "Lõi"; }
public abstract class Decorator : IComponent
{
    protected IComponent _inner;
    protected Decorator(IComponent c) => _inner = c;
    public virtual string Operation() => _inner.Operation();
}
public class DecoratorA : Decorator { public DecoratorA(IComponent c) : base(c) { } public override string Operation() => $"A({_inner.Operation()})"; }
public class DecoratorB : Decorator { public DecoratorB(IComponent c) : base(c) { } public override string Operation() => $"B({_inner.Operation()})"; }
''', H + r'''
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
'''))

ITEMS.append(("Structural", "Facade", "DatHangMotCham", H + r'''
Console.WriteLine("=== FACADE (mẫu chuẩn) ===");
new Facade().Operation();

public class SubsystemA { public string Op1() => "A: sẵn sàng"; public string OpN() => "A: chạy!"; }
public class SubsystemB { public string Op1() => "B: sẵn sàng"; public string OpZ() => "B: chạy!"; }
public class Facade
{
    private readonly SubsystemA _a = new(); private readonly SubsystemB _b = new();
    public void Operation()
    {
        Console.WriteLine(_a.Op1()); Console.WriteLine(_b.Op1());
        Console.WriteLine(_a.OpN()); Console.WriteLine(_b.OpZ());
    }
}
''', H + r'''
Console.WriteLine("=== FACADE: Nút Đặt hàng 1-chạm ===");
var facade = new CheckoutFacade(new InventoryService(), new PaymentService(), new ShippingService(), new NotificationService());

var ok = new CheckoutOrder { Id = "DH01", Customer = "An", Product = "iPhone", Qty = 1, Total = 20_000_000 };
Console.WriteLine($"=> Kết quả: {(facade.PlaceOrder(ok) ? "THÀNH CÔNG" : "THẤT BẠI")}\n");

var fail = new CheckoutOrder { Id = "DH02", Customer = "Bình", Product = "iPhone", Qty = 999, Total = 1_000_000 };
Console.WriteLine($"=> Kết quả: {(facade.PlaceOrder(fail) ? "THÀNH CÔNG" : "THẤT BẠI")}");

public class CheckoutOrder { public string Id, Customer, Product; public int Qty; public decimal Total; }

public class InventoryService
{
    private int _stock = 10;
    public bool ReserveStock(CheckoutOrder o) { if (o.Qty > _stock) { Console.WriteLine("  [Kho] Không đủ hàng."); return false; } _stock -= o.Qty; Console.WriteLine($"  [Kho] Đã giữ {o.Qty} {o.Product}."); return true; }
    public void Release(CheckoutOrder o) { _stock += o.Qty; Console.WriteLine("  [Kho] Hoàn kho."); }
}
public class PaymentService { public bool Charge(string c, decimal amt) { Console.WriteLine($"  [Ví] Trừ {amt:N0} của {c}."); return true; } }
public class ShippingService { public string CreateWaybill(CheckoutOrder o) { var w = "VD-" + o.Id; Console.WriteLine($"  [Vận chuyển] Tạo vận đơn {w}."); return w; } }
public class NotificationService { public void Send(string c, string msg) => Console.WriteLine($"  [SMS/Email] Gửi {c}: {msg}"); }

public class CheckoutFacade
{
    private readonly InventoryService _inv; private readonly PaymentService _pay;
    private readonly ShippingService _ship; private readonly NotificationService _noti;
    public CheckoutFacade(InventoryService i, PaymentService p, ShippingService s, NotificationService n) { _inv = i; _pay = p; _ship = s; _noti = n; }

    public bool PlaceOrder(CheckoutOrder order)   // Client chỉ gọi 1 phương thức duy nhất
    {
        Console.WriteLine($"Đặt hàng {order.Id}...");
        if (!_inv.ReserveStock(order)) return false;
        if (!_pay.Charge(order.Customer, order.Total)) { _inv.Release(order); return false; }
        var waybill = _ship.CreateWaybill(order);
        _noti.Send(order.Customer, $"Đơn {order.Id} thành công, vận đơn {waybill}");
        return true;
    }
}
'''))

ITEMS.append(("Structural", "Flyweight", "ToiUuBoNhoSanPham", H + r'''
Console.WriteLine("=== FLYWEIGHT (mẫu chuẩn) ===");
var factory = new TreeTypeFactory();
var forest = new List<Tree>();
var rnd = new Random(1);
for (int i = 0; i < 1000; i++)
    forest.Add(new Tree(rnd.Next(100), rnd.Next(100), factory.Get(i % 2 == 0 ? "Sồi" : "Thông", "Xanh")));
Console.WriteLine($"Số cây: {forest.Count}, số TreeType thực sự trong RAM: {factory.Count}");

public class TreeType
{
    public string Name, Color;   // Intrinsic (chia sẻ)
    public TreeType(string n, string c) { Name = n; Color = c; }
}
public class TreeTypeFactory
{
    private readonly Dictionary<string, TreeType> _cache = new();
    public int Count => _cache.Count;
    public TreeType Get(string n, string c)
    {
        var k = n + "|" + c;
        if (!_cache.TryGetValue(k, out var t)) _cache[k] = t = new TreeType(n, c);
        return t;
    }
}
public class Tree { public int X, Y; public TreeType Type; public Tree(int x, int y, TreeType t) { X = x; Y = y; Type = t; } }   // X,Y: Extrinsic
''', H + r'''
Console.WriteLine("=== FLYWEIGHT: Tối ưu bộ nhớ thông số sản phẩm ===");
var factory = new ProductSpecificationFactory();
var orderItems = new List<OrderItem>();
var rnd = new Random(7);
string[] models = { "iPhone 16 128GB", "iPhone 16 256GB", "iPhone 16 Pro 256GB" };

for (int i = 0; i < 100_000; i++)
{
    var spec = factory.Get(models[i % 3]);   // dùng chung
    orderItems.Add(new OrderItem { SerialNumber = $"IMEI{i:D8}", SoldPrice = 20_000_000 + rnd.Next(0, 3_000_000), Spec = spec });
}

Console.WriteLine($"Số dòng đơn hàng      : {orderItems.Count:N0}");
Console.WriteLine($"Số ProductSpecification thực tế trong RAM: {factory.Count}");
Console.WriteLine($"Ví dụ: {orderItems[0].SerialNumber} -> {orderItems[0].Spec.ModelName} ({orderItems[0].Spec.TechnicalSpecs})");
Console.WriteLine($"Cùng model dùng chung 1 đối tượng? {ReferenceEquals(orderItems[0].Spec, orderItems[3].Spec)}");

// Intrinsic: dùng chung
public class ProductSpecification
{
    public string ModelName { get; }
    public string TechnicalSpecs { get; }
    public byte[] ImageBytes { get; }
    public ProductSpecification(string model) { ModelName = model; TechnicalSpecs = "Chip A18, OLED 6.1\", " + model; ImageBytes = new byte[1024 * 100]; }
}
public class ProductSpecificationFactory
{
    private readonly Dictionary<string, ProductSpecification> _pool = new();
    public int Count => _pool.Count;
    public ProductSpecification Get(string model)
    {
        if (!_pool.TryGetValue(model, out var s)) _pool[model] = s = new ProductSpecification(model);
        return s;
    }
}
// Extrinsic: riêng từng giao dịch
public class OrderItem
{
    public string SerialNumber { get; set; }
    public decimal SoldPrice { get; set; }
    public ProductSpecification Spec { get; set; }
}
'''))

ITEMS.append(("Structural", "Proxy", "DemDanhMucSanPham", H + r'''
Console.WriteLine("=== PROXY (mẫu chuẩn - Protection Proxy) ===");
ISubject real = new RealSubject();
ISubject proxy = new Proxy(real, isAdmin: false);
proxy.Request();
proxy = new Proxy(real, isAdmin: true);
proxy.Request();

public interface ISubject { void Request(); }
public class RealSubject : ISubject { public void Request() => Console.WriteLine("RealSubject: xử lý yêu cầu."); }
public class Proxy : ISubject
{
    private readonly ISubject _real; private readonly bool _isAdmin;
    public Proxy(ISubject r, bool isAdmin) { _real = r; _isAdmin = isAdmin; }
    public void Request()
    {
        if (!_isAdmin) { Console.WriteLine("Proxy: TỪ CHỐI truy cập."); return; }
        Console.WriteLine("Proxy: kiểm tra quyền OK."); _real.Request();
    }
}
''', H + r'''
Console.WriteLine("=== PROXY: Bộ nhớ đệm danh mục sản phẩm ===");
var real = new RealProductService();
IProductService service = new ProductServiceProxy(real, new InMemoryCache());

for (int i = 1; i <= 3; i++)
{
    var p = service.GetById(101);
    Console.WriteLine($"Lần {i}: {p.Name} - {p.Price:N0}");
}
service.GetById(102);
Console.WriteLine($"\nTổng số lần chạm CSDL thật: {real.DbHits} (thay vì 4)");

public class Product { public int Id; public string Name; public decimal Price; }
public interface IProductService { Product GetById(int id); }

public class RealProductService : IProductService
{
    public int DbHits { get; private set; }
    public Product GetById(int id)
    {
        DbHits++;
        Console.WriteLine($"   [SQL] SELECT * FROM Products WHERE Id={id}");
        Thread.Sleep(100);   // mô phỏng truy vấn chậm
        return new Product { Id = id, Name = $"Sản phẩm #{id}", Price = 150000 + id };
    }
}
public interface ICache { T Get<T>(string key) where T : class; void Set<T>(string key, T v, TimeSpan ttl) where T : class; }
public class InMemoryCache : ICache
{
    private readonly Dictionary<string, (object v, DateTime exp)> _d = new();
    public T Get<T>(string key) where T : class => _d.TryGetValue(key, out var e) && e.exp > DateTime.Now ? e.v as T : null;
    public void Set<T>(string key, T v, TimeSpan ttl) where T : class => _d[key] = (v, DateTime.Now + ttl);
}
public class ProductServiceProxy : IProductService
{
    private readonly RealProductService _real; private readonly ICache _cache;
    public ProductServiceProxy(RealProductService r, ICache c) { _real = r; _cache = c; }
    public Product GetById(int id)
    {
        var cached = _cache.Get<Product>($"prod:{id}");
        if (cached != null) { Console.WriteLine("   [Cache HIT]"); return cached; }
        var data = _real.GetById(id);                       // Cache miss -> đọc SQL
        _cache.Set($"prod:{id}", data, TimeSpan.FromMinutes(30));
        return data;
    }
}
'''))
