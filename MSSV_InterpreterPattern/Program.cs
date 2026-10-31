Console.OutputEncoding = System.Text.Encoding.UTF8;

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
