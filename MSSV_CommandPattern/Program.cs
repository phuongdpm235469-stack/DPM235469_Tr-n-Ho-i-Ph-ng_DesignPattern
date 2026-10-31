Console.OutputEncoding = System.Text.Encoding.UTF8;

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
