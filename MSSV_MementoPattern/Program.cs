Console.OutputEncoding = System.Text.Encoding.UTF8;

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
