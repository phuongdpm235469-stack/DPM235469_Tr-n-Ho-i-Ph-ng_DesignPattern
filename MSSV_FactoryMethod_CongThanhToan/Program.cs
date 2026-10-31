Console.OutputEncoding = System.Text.Encoding.UTF8;

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
