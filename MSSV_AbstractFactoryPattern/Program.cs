Console.OutputEncoding = System.Text.Encoding.UTF8;

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
