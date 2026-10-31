Console.OutputEncoding = System.Text.Encoding.UTF8;

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
