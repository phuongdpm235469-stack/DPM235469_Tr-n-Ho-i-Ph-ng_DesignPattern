Console.OutputEncoding = System.Text.Encoding.UTF8;

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
