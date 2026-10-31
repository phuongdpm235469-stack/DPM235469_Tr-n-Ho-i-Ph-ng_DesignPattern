from data_cs import H

ITEMS_B = []

ITEMS_B.append(("Behavioral", "ChainOfResponsibility", "DuyetGiamGia", H + r'''
Console.WriteLine("=== CHAIN OF RESPONSIBILITY (mẫu chuẩn) ===");
var a = new ConcreteHandler("A", 10);
var b = new ConcreteHandler("B", 20);
var c = new ConcreteHandler("C", 30);
a.SetNext(b).SetNext(c);
foreach (var v in new[] { 5, 18, 29, 50 }) a.Handle(v);

public abstract class Handler
{
    private Handler _next;
    public Handler SetNext(Handler n) { _next = n; return n; }
    public virtual void Handle(int request)
    {
        if (_next != null) _next.Handle(request);
        else Console.WriteLine($"Yêu cầu {request}: không ai xử lý được.");
    }
}
public class ConcreteHandler : Handler
{
    private readonly string _name; private readonly int _limit;
    public ConcreteHandler(string n, int limit) { _name = n; _limit = limit; }
    public override void Handle(int r)
    {
        if (r <= _limit) Console.WriteLine($"Yêu cầu {r}: {_name} xử lý.");
        else base.Handle(r);
    }
}
''', H + r'''
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
'''))

ITEMS_B.append(("Behavioral", "Command", "ThaoTacGioHang", H + r'''
Console.WriteLine("=== COMMAND (mẫu chuẩn) ===");
var light = new Light();
var inv = new Invoker();
inv.Run(new OnCommand(light));
inv.Run(new OffCommand(light));
inv.Undo();
inv.Undo();

public class Light { public bool On; public void Set(bool v) { On = v; Console.WriteLine($"Đèn: {(On ? "BẬT" : "TẮT")}"); } }
public interface ICommand { void Execute(); void Undo(); }
public class OnCommand : ICommand { private readonly Light _l; public OnCommand(Light l) => _l = l; public void Execute() => _l.Set(true); public void Undo() => _l.Set(false); }
public class OffCommand : ICommand { private readonly Light _l; public OffCommand(Light l) => _l = l; public void Execute() => _l.Set(false); public void Undo() => _l.Set(true); }
public class Invoker
{
    private readonly Stack<ICommand> _history = new();
    public void Run(ICommand c) { c.Execute(); _history.Push(c); }
    public void Undo() { if (_history.Count > 0) _history.Pop().Undo(); }
}
''', H + r'''
Console.WriteLine("=== COMMAND: Thao tác giỏ hàng có Undo ===");
var cart = new ShoppingCart();
var mgr = new CartCommandManager();

mgr.Run(new AddItemCommand(cart, "Áo thun", 2, 150000));
mgr.Run(new AddItemCommand(cart, "Quần jean", 1, 400000));
mgr.Run(new RemoveItemCommand(cart, "Áo thun"));
cart.Print();

Console.WriteLine("\n-- Hoàn tác 2 thao tác --");
mgr.Undo(); mgr.Undo();
cart.Print();

public class ShoppingCart
{
    public Dictionary<string, (int Qty, decimal Price)> Items { get; } = new();
    public void Print() => Console.WriteLine("Giỏ: " + (Items.Count == 0 ? "(trống)" : string.Join("; ", Items.Select(i => $"{i.Key} x{i.Value.Qty}"))) + $" | Tổng {Items.Sum(i => i.Value.Qty * i.Value.Price):N0}");
}
public interface ICartCommand { void Execute(); void Undo(); }
public class AddItemCommand : ICartCommand
{
    private readonly ShoppingCart _c; private readonly string _n; private readonly int _q; private readonly decimal _p;
    public AddItemCommand(ShoppingCart c, string n, int q, decimal p) { _c = c; _n = n; _q = q; _p = p; }
    public void Execute() { _c.Items[_n] = (_q, _p); Console.WriteLine($"+ Thêm {_n}"); }
    public void Undo() { _c.Items.Remove(_n); Console.WriteLine($"~ Hoàn tác thêm {_n}"); }
}
public class RemoveItemCommand : ICartCommand
{
    private readonly ShoppingCart _c; private readonly string _n; private (int Qty, decimal Price) _backup;
    public RemoveItemCommand(ShoppingCart c, string n) { _c = c; _n = n; }
    public void Execute() { _backup = _c.Items[_n]; _c.Items.Remove(_n); Console.WriteLine($"- Xóa {_n}"); }
    public void Undo() { _c.Items[_n] = _backup; Console.WriteLine($"~ Hoàn tác xóa {_n}"); }
}
public class CartCommandManager
{
    private readonly Stack<ICartCommand> _history = new();
    public void Run(ICartCommand c) { c.Execute(); _history.Push(c); }
    public void Undo() { if (_history.Count > 0) _history.Pop().Undo(); }
}
'''))

ITEMS_B.append(("Behavioral", "Iterator", "LichSuDonHang", H + r'''
Console.WriteLine("=== ITERATOR (mẫu chuẩn) ===");
var col = new WordCollection();
col.Add("một"); col.Add("hai"); col.Add("ba");
Console.WriteLine("Thuận:");
for (var it = col.CreateIterator(); it.HasNext();) Console.WriteLine("  " + it.Next());
Console.WriteLine("Ngược:");
for (var it = col.CreateReverseIterator(); it.HasNext();) Console.WriteLine("  " + it.Next());

public interface IIterator<T> { bool HasNext(); T Next(); }
public class WordCollection
{
    private readonly List<string> _items = new();
    public void Add(string s) => _items.Add(s);
    public int Count => _items.Count;
    public string this[int i] => _items[i];
    public IIterator<string> CreateIterator() => new ForwardIterator(this);
    public IIterator<string> CreateReverseIterator() => new ReverseIterator(this);
}
public class ForwardIterator : IIterator<string>
{
    private readonly WordCollection _c; private int _i;
    public ForwardIterator(WordCollection c) => _c = c;
    public bool HasNext() => _i < _c.Count;
    public string Next() => _c[_i++];
}
public class ReverseIterator : IIterator<string>
{
    private readonly WordCollection _c; private int _i;
    public ReverseIterator(WordCollection c) { _c = c; _i = c.Count - 1; }
    public bool HasNext() => _i >= 0;
    public string Next() => _c[_i--];
}
''', H + r'''
Console.WriteLine("=== ITERATOR: Duyệt lịch sử đơn hàng ===");
var history = new OrderHistory();
history.Add(new OrderRecord("HD-1001", "An", 500000, true));
history.Add(new OrderRecord("HD-1002", "Bình", 1200000, false));
history.Add(new OrderRecord("HD-1003", "Chi", 300000, true));
history.Add(new OrderRecord("HD-1004", "Dũng", 900000, false));

Console.WriteLine("-- Đơn mới nhất trước --");
for (var it = history.NewestFirst(); it.HasNext();) Console.WriteLine("  " + it.Next());

Console.WriteLine("-- Chỉ các đơn CHƯA thanh toán --");
for (var it = history.UnpaidOnly(); it.HasNext();) Console.WriteLine("  " + it.Next());

public record OrderRecord(string Id, string Customer, decimal Total, bool Paid)
{
    public override string ToString() => $"{Id} | {Customer} | {Total:N0} | {(Paid ? "Đã TT" : "Chưa TT")}";
}
public interface IOrderIterator { bool HasNext(); OrderRecord Next(); }
public class OrderHistory
{
    private readonly List<OrderRecord> _list = new();
    public void Add(OrderRecord r) => _list.Add(r);
    public IOrderIterator NewestFirst() => new ListIterator(_list.AsEnumerable().Reverse().ToList());
    public IOrderIterator UnpaidOnly() => new ListIterator(_list.Where(o => !o.Paid).ToList());
}
public class ListIterator : IOrderIterator
{
    private readonly List<OrderRecord> _l; private int _i;
    public ListIterator(List<OrderRecord> l) => _l = l;
    public bool HasNext() => _i < _l.Count;
    public OrderRecord Next() => _l[_i++];
}
'''))

ITEMS_B.append(("Behavioral", "Mediator", "ManHinhBanHang", H + r'''
Console.WriteLine("=== MEDIATOR (mẫu chuẩn) ===");
var m = new ConcreteMediator();
m.A = new ComponentA(m); m.B = new ComponentB(m);
m.A.DoA();
m.B.DoB();

public interface IMediator { void Notify(object sender, string ev); }
public class ComponentA { private readonly IMediator _m; public ComponentA(IMediator m) => _m = m; public void DoA() { Console.WriteLine("A làm việc"); _m.Notify(this, "A"); } public void React() => Console.WriteLine("A phản ứng"); }
public class ComponentB { private readonly IMediator _m; public ComponentB(IMediator m) => _m = m; public void DoB() { Console.WriteLine("B làm việc"); _m.Notify(this, "B"); } public void React() => Console.WriteLine("B phản ứng"); }
public class ConcreteMediator : IMediator
{
    public ComponentA A; public ComponentB B;
    public void Notify(object sender, string ev) { if (ev == "A") B.React(); else if (ev == "B") A.React(); }
}
''', H + r'''
Console.WriteLine("=== MEDIATOR: Điều phối màn hình bán hàng ===");
var screen = new SalesScreenMediator();
screen.Qty = new QuantityBox(screen);
screen.Total = new TotalLabel();
screen.Pay = new PayButton();
screen.Customer = new CustomerBox(screen);

screen.Qty.UnitPrice = 250000;
screen.Qty.SetQty(0);
screen.Qty.SetQty(3);
screen.Customer.Select("VIP");
screen.Qty.SetQty(4);

public interface ISalesMediator { void Notify(object sender, string ev); }
public class QuantityBox
{
    private readonly ISalesMediator _m; public int Qty; public decimal UnitPrice;
    public QuantityBox(ISalesMediator m) => _m = m;
    public void SetQty(int q) { Console.WriteLine($"> Nhập số lượng = {q}"); Qty = q; _m.Notify(this, "QtyChanged"); }
}
public class CustomerBox
{
    private readonly ISalesMediator _m; public string Type = "Thường";
    public CustomerBox(ISalesMediator m) => _m = m;
    public void Select(string t) { Console.WriteLine($"> Chọn khách hàng loại {t}"); Type = t; _m.Notify(this, "CustomerChanged"); }
}
public class TotalLabel { public void Show(decimal v) => Console.WriteLine($"   [Label] Thành tiền: {v:N0}"); }
public class PayButton { public void SetEnabled(bool e) => Console.WriteLine($"   [Nút Thanh toán] {(e ? "BẬT" : "TẮT")}"); }

public class SalesScreenMediator : ISalesMediator
{
    public QuantityBox Qty; public TotalLabel Total; public PayButton Pay; public CustomerBox Customer;
    public void Notify(object sender, string ev)
    {
        if (ev == "QtyChanged" || ev == "CustomerChanged")
        {
            var sum = Qty.Qty * Qty.UnitPrice;
            if (Customer.Type == "VIP") sum *= 0.9m;
            Total.Show(sum);
            Pay.SetEnabled(Qty.Qty > 0);
        }
    }
}
'''))

ITEMS_B.append(("Behavioral", "Memento", "HoanTacGioHang", H + r'''
Console.WriteLine("=== MEMENTO (mẫu chuẩn) ===");
var editor = new Editor();
var care = new Caretaker(editor);
editor.Text = "Phiên bản 1"; care.Backup();
editor.Text = "Phiên bản 2"; care.Backup();
editor.Text = "Phiên bản 3 (hỏng)";
Console.WriteLine("Hiện tại: " + editor.Text);
care.Undo(); Console.WriteLine("Sau undo: " + editor.Text);
care.Undo(); Console.WriteLine("Sau undo: " + editor.Text);

public class Editor
{
    public string Text { get; set; }
    public Memento Save() => new Memento(Text);
    public void Restore(Memento m) => Text = m.State;
    public class Memento { public string State { get; } internal Memento(string s) => State = s; }
}
public class Caretaker
{
    private readonly Stack<Editor.Memento> _s = new(); private readonly Editor _e;
    public Caretaker(Editor e) => _e = e;
    public void Backup() => _s.Push(_e.Save());
    public void Undo() { if (_s.Count > 0) _e.Restore(_s.Pop()); }
}
''', H + r'''
Console.WriteLine("=== MEMENTO: Hoàn tác giỏ hàng bằng snapshot ===");
var cart = new Cart();
var history = new CartHistory();

cart.Add("Áo thun", 150000); history.Save(cart.CreateSnapshot());
cart.Add("Quần jean", 400000); history.Save(cart.CreateSnapshot());
cart.Add("Giày thể thao", 900000);
cart.Print("Hiện tại");

cart.Restore(history.Pop()); cart.Print("Sau hoàn tác 1");
cart.Restore(history.Pop()); cart.Print("Sau hoàn tác 2");

public class CartSnapshot
{
    public IReadOnlyDictionary<string, decimal> Items { get; }
    public CartSnapshot(Dictionary<string, decimal> items) => Items = new Dictionary<string, decimal>(items);
}
public class Cart
{
    private Dictionary<string, decimal> _items = new();
    public void Add(string name, decimal price) => _items[name] = price;
    public CartSnapshot CreateSnapshot() => new CartSnapshot(_items);
    public void Restore(CartSnapshot s) => _items = new Dictionary<string, decimal>(s.Items);
    public void Print(string label) => Console.WriteLine($"[{label}] {string.Join(", ", _items.Keys)} | Tổng: {_items.Values.Sum():N0}");
}
public class CartHistory
{
    private readonly Stack<CartSnapshot> _stack = new();
    public void Save(CartSnapshot s) => _stack.Push(s);
    public CartSnapshot Pop() => _stack.Pop();
}
'''))

ITEMS_B.append(("Behavioral", "Observer", "CanhBaoTonKho", H + r'''
Console.WriteLine("=== OBSERVER (mẫu chuẩn) ===");
var subject = new Subject();
var o1 = new ConcreteObserver("O1");
var o2 = new ConcreteObserver("O2");
subject.Attach(o1); subject.Attach(o2);
subject.State = 10;
subject.Detach(o1);
subject.State = 20;

public interface IObserver { void Update(int state); }
public class Subject
{
    private readonly List<IObserver> _obs = new(); private int _state;
    public int State { get => _state; set { _state = value; Notify(); } }
    public void Attach(IObserver o) => _obs.Add(o);
    public void Detach(IObserver o) => _obs.Remove(o);
    private void Notify() { foreach (var o in _obs) o.Update(_state); }
}
public class ConcreteObserver : IObserver
{
    private readonly string _n; public ConcreteObserver(string n) => _n = n;
    public void Update(int s) => Console.WriteLine($"{_n} nhận trạng thái mới: {s}");
}
''', H + r'''
Console.WriteLine("=== OBSERVER: Cảnh báo tồn kho ===");
var product = new StockProduct("Laptop Dell XPS", 10);
product.Attach(new WarehouseObserver());
product.Attach(new PurchasingObserver());
product.Attach(new WebsiteObserver());

product.Sell(4);
product.Sell(4);   // còn 2 -> kích hoạt cảnh báo
product.Sell(2);   // hết hàng

public interface IStockObserver { void OnStockChanged(StockProduct p); }
public class StockProduct
{
    private readonly List<IStockObserver> _obs = new();
    public string Name { get; } public int Stock { get; private set; }
    public StockProduct(string name, int stock) { Name = name; Stock = stock; }
    public void Attach(IStockObserver o) => _obs.Add(o);
    public void Detach(IStockObserver o) => _obs.Remove(o);
    public void Sell(int qty)
    {
        Stock -= qty;
        Console.WriteLine($"\nBán {qty} {Name}, tồn kho còn {Stock}");
        foreach (var o in _obs) o.OnStockChanged(this);
    }
}
public class WarehouseObserver : IStockObserver
{
    public void OnStockChanged(StockProduct p) { if (p.Stock <= 3) Console.WriteLine($"   [Kho] Cảnh báo: {p.Name} sắp hết ({p.Stock})."); }
}
public class PurchasingObserver : IStockObserver
{
    public void OnStockChanged(StockProduct p) { if (p.Stock <= 3) Console.WriteLine($"   [Mua hàng] Tạo đề nghị nhập thêm {p.Name}."); }
}
public class WebsiteObserver : IStockObserver
{
    public void OnStockChanged(StockProduct p) { if (p.Stock == 0) Console.WriteLine($"   [Website] Chuyển {p.Name} sang 'Hết hàng'."); }
}
'''))

ITEMS_B.append(("Behavioral", "State", "TrangThaiDonHang", H + r'''
Console.WriteLine("=== STATE (mẫu chuẩn) ===");
var ctx = new Context(new StateA());
ctx.Request();
ctx.Request();
ctx.Request();

public class Context
{
    private IState _state;
    public Context(IState s) => _state = s;
    public void TransitionTo(IState s) { Console.WriteLine($"  -> chuyển sang {s.GetType().Name}"); _state = s; }
    public void Request() => _state.Handle(this);
}
public interface IState { void Handle(Context c); }
public class StateA : IState { public void Handle(Context c) { Console.WriteLine("StateA xử lý"); c.TransitionTo(new StateB()); } }
public class StateB : IState { public void Handle(Context c) { Console.WriteLine("StateB xử lý"); c.TransitionTo(new StateA()); } }
''', H + r'''
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
'''))

ITEMS_B.append(("Behavioral", "Strategy", "ChinhSachGiamGia", H + r'''
Console.WriteLine("=== STRATEGY (mẫu chuẩn) ===");
var calc = new Calculator(new Add());
Console.WriteLine($"f(10, 5) = {calc.Run(10, 5)}");
calc.SetStrategy(new Multiply());
Console.WriteLine($"f(10, 5) = {calc.Run(10, 5)}");

public interface IStrategy { int Execute(int a, int b); }
public class Add : IStrategy { public int Execute(int a, int b) => a + b; }
public class Multiply : IStrategy { public int Execute(int a, int b) => a * b; }
public class Calculator
{
    private IStrategy _s;
    public Calculator(IStrategy s) => _s = s;
    public void SetStrategy(IStrategy s) => _s = s;
    public int Run(int a, int b) => _s.Execute(a, b);
}
''', H + r'''
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
'''))

ITEMS_B.append(("Behavioral", "TemplateMethod", "QuyTrinhXuLyDon", H + r'''
Console.WriteLine("=== TEMPLATE METHOD (mẫu chuẩn) ===");
new ConcreteA().TemplateMethod();
Console.WriteLine();
new ConcreteB().TemplateMethod();

public abstract class AbstractClass
{
    public void TemplateMethod()
    {
        Step1(); Step2(); Hook(); Step3();
    }
    protected void Step1() => Console.WriteLine("Bước 1 (cố định)");
    protected abstract void Step2();
    protected virtual void Hook() { }
    protected void Step3() => Console.WriteLine("Bước 3 (cố định)");
}
public class ConcreteA : AbstractClass { protected override void Step2() => Console.WriteLine("Bước 2 của A"); }
public class ConcreteB : AbstractClass
{
    protected override void Step2() => Console.WriteLine("Bước 2 của B");
    protected override void Hook() => Console.WriteLine("Hook của B");
}
''', H + r'''
Console.WriteLine("=== TEMPLATE METHOD: Quy trình xử lý đơn hàng ===");
OrderProcessor[] processors = { new RetailOrderProcessor(), new WholesaleOrderProcessor() };
foreach (var p in processors) { p.Process("HD-3001", 100); Console.WriteLine(); }

public abstract class OrderProcessor
{
    // Template method: khung quy trình cố định
    public void Process(string orderId, int qty)
    {
        Console.WriteLine($"--- {GetType().Name} xử lý {orderId} ---");
        Validate(orderId, qty);
        var price = CalculatePrice(qty);
        TakePayment(price);
        Ship(orderId);
        AfterSales(orderId);   // hook
    }
    protected void Validate(string id, int qty) => Console.WriteLine($"1. Kiểm tra đơn {id}, số lượng {qty}: hợp lệ");
    protected abstract decimal CalculatePrice(int qty);
    protected abstract void TakePayment(decimal amount);
    protected virtual void Ship(string id) => Console.WriteLine($"4. Giao hàng tiêu chuẩn cho {id}");
    protected virtual void AfterSales(string id) { }
}
public class RetailOrderProcessor : OrderProcessor
{
    protected override decimal CalculatePrice(int qty) { var p = qty * 100_000m; Console.WriteLine($"2. Giá bán lẻ: {p:N0}"); return p; }
    protected override void TakePayment(decimal a) => Console.WriteLine($"3. Thu {a:N0} ngay tại quầy/online");
}
public class WholesaleOrderProcessor : OrderProcessor
{
    protected override decimal CalculatePrice(int qty) { var p = qty * 100_000m * 0.8m; Console.WriteLine($"2. Giá sỉ (-20%): {p:N0}"); return p; }
    protected override void TakePayment(decimal a) => Console.WriteLine($"3. Ghi công nợ {a:N0} (30 ngày)");
    protected override void Ship(string id) => Console.WriteLine($"4. Giao hàng nguyên pallet cho đại lý {id}");
    protected override void AfterSales(string id) => Console.WriteLine($"5. Gửi bảng đối chiếu công nợ cho {id}");
}
'''))

ITEMS_B.append(("Behavioral", "Visitor", "TinhThueTheoLoaiHang", H + r'''
Console.WriteLine("=== VISITOR (mẫu chuẩn) ===");
var elements = new List<IElement> { new ElementA(), new ElementB() };
foreach (var e in elements) e.Accept(new PrintVisitor());
foreach (var e in elements) e.Accept(new ExportVisitor());

public interface IVisitor { void Visit(ElementA a); void Visit(ElementB b); }
public interface IElement { void Accept(IVisitor v); }
public class ElementA : IElement { public string ExclusiveA() => "A"; public void Accept(IVisitor v) => v.Visit(this); }
public class ElementB : IElement { public string ExclusiveB() => "B"; public void Accept(IVisitor v) => v.Visit(this); }
public class PrintVisitor : IVisitor
{
    public void Visit(ElementA a) => Console.WriteLine("Print: " + a.ExclusiveA());
    public void Visit(ElementB b) => Console.WriteLine("Print: " + b.ExclusiveB());
}
public class ExportVisitor : IVisitor
{
    public void Visit(ElementA a) => Console.WriteLine("Export JSON A");
    public void Visit(ElementB b) => Console.WriteLine("Export JSON B");
}
''', H + r'''
Console.WriteLine("=== VISITOR: Tính thuế & phí theo loại hàng ===");
var cart = new List<IProductElement>
{
    new Food("Gạo ST25", 200_000),
    new Electronics("Tai nghe Bluetooth", 1_500_000),
    new Clothing("Áo khoác", 800_000)
};

var tax = new TaxVisitor();
var ship = new ShippingFeeVisitor();
foreach (var p in cart) { p.Accept(tax); p.Accept(ship); }
Console.WriteLine($"\nTổng thuế : {tax.Total:N0}");
Console.WriteLine($"Tổng phí ship: {ship.Total:N0}");

public interface IProductVisitor
{
    void Visit(Food f); void Visit(Electronics e); void Visit(Clothing c);
}
public interface IProductElement { void Accept(IProductVisitor v); }
public class Food : IProductElement
{
    public string Name { get; } public decimal Price { get; }
    public Food(string n, decimal p) { Name = n; Price = p; }
    public void Accept(IProductVisitor v) => v.Visit(this);
}
public class Electronics : IProductElement
{
    public string Name { get; } public decimal Price { get; }
    public Electronics(string n, decimal p) { Name = n; Price = p; }
    public void Accept(IProductVisitor v) => v.Visit(this);
}
public class Clothing : IProductElement
{
    public string Name { get; } public decimal Price { get; }
    public Clothing(string n, decimal p) { Name = n; Price = p; }
    public void Accept(IProductVisitor v) => v.Visit(this);
}
// Thêm phép toán mới chỉ cần thêm Visitor, không sửa các lớp sản phẩm
public class TaxVisitor : IProductVisitor
{
    public decimal Total { get; private set; }
    private void Add(string n, decimal t, decimal rate) { Total += t; Console.WriteLine($"[Thuế {rate:P0}] {n}: {t:N0}"); }
    public void Visit(Food f) => Add(f.Name, f.Price * 0.05m, 0.05m);
    public void Visit(Electronics e) => Add(e.Name, e.Price * 0.10m, 0.10m);
    public void Visit(Clothing c) => Add(c.Name, c.Price * 0.08m, 0.08m);
}
public class ShippingFeeVisitor : IProductVisitor
{
    public decimal Total { get; private set; }
    private void Add(string n, decimal fee) { Total += fee; Console.WriteLine($"[Ship] {n}: {fee:N0}"); }
    public void Visit(Food f) => Add(f.Name, 20_000);
    public void Visit(Electronics e) => Add(e.Name, 35_000);
    public void Visit(Clothing c) => Add(c.Name, 15_000);
}
'''))

ITEMS_B.append(("Behavioral", "Interpreter", "QuyTacCoupon", H + r'''
Console.WriteLine("=== INTERPRETER (mẫu chuẩn) ===");
// (A AND B) OR (NOT C)
IExpression expr = new OrExpr(
    new AndExpr(new Var("A"), new Var("B")),
    new NotExpr(new Var("C")));
var ctx = new Dictionary<string, bool> { ["A"] = true, ["B"] = false, ["C"] = false };
Console.WriteLine($"(A AND B) OR (NOT C) với A=1,B=0,C=0 => {expr.Interpret(ctx)}");
ctx["C"] = true;
Console.WriteLine($"(A AND B) OR (NOT C) với A=1,B=0,C=1 => {expr.Interpret(ctx)}");

public interface IExpression { bool Interpret(Dictionary<string, bool> ctx); }
public class Var : IExpression { private readonly string _n; public Var(string n) => _n = n; public bool Interpret(Dictionary<string, bool> c) => c[_n]; }
public class AndExpr : IExpression { private readonly IExpression _l, _r; public AndExpr(IExpression l, IExpression r) { _l = l; _r = r; } public bool Interpret(Dictionary<string, bool> c) => _l.Interpret(c) && _r.Interpret(c); }
public class OrExpr : IExpression { private readonly IExpression _l, _r; public OrExpr(IExpression l, IExpression r) { _l = l; _r = r; } public bool Interpret(Dictionary<string, bool> c) => _l.Interpret(c) || _r.Interpret(c); }
public class NotExpr : IExpression { private readonly IExpression _e; public NotExpr(IExpression e) => _e = e; public bool Interpret(Dictionary<string, bool> c) => !_e.Interpret(c); }
''', H + r'''
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
'''))
