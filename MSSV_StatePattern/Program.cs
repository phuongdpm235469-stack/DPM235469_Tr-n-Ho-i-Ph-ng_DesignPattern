Console.OutputEncoding = System.Text.Encoding.UTF8;

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
