Console.OutputEncoding = System.Text.Encoding.UTF8;

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
