from ast import *
from utils import input_int, add64, sub64, neg64


# This version is for InterpLvar to inherit from
class InterpLint:
    def interp_exp(self, e, env):
        match e:
            case BinOp(left, Add(), right):
                l = self.interp_exp(left, env)
                r = self.interp_exp(right, env)
                return add64(l, r)
            case BinOp(left, Sub(), right):
                l = self.interp_exp(left, env)
                r = self.interp_exp(right, env)
                return sub64(l, r)
            case UnaryOp(USub(), v):
                return neg64(self.interp_exp(v, env))
            case Constant(value):
                return value
            case Call(Name("input_int"), []):
                return input_int()
            case _:
                raise Exception("error in interp_exp, unexpected " + repr(e))

    def interp_stmt(self, s, env, cont):
        match s:
            case Expr(Call(Name("print"), [arg])):
                val = self.interp_exp(arg, env)
                print(val, end="")
                return self.interp_stmts(cont, env)
            case Expr(value):
                self.interp_exp(value, env)
                return self.interp_stmts(cont, env)
            case _:
                raise Exception("error in interp_stmt, unexpected " + repr(s))

    def interp_stmts(self, ss, env):
        match ss:
            case []:
                return 0
            case [s, *ss]:
                return self.interp_stmt(s, env, ss)

    def interp(self, p):
        match p:
            case Module(body):
                self.interp_stmts(body, {})
            case _:
                raise Exception("error in interp, unexpected " + repr(p))


##################################################################################
class PeLint:
    def pe_neg(self, r):
        match r:
            case Constant(n):
                return Constant(neg64(n))
            case _:
                return UnaryOp(USub(), r)

    def pe_add(self, r1, r2):
        match (r1, r2):
            case (Constant(n1), Constant(n2)):
                return Constant(add64(n1, n2))
            case _:
                return BinOp(r1, Add(), r2)

    def pe_sub(self, r1, r2):
        match (r1, r2):
            case (Constant(n1), Constant(n2)):
                return Constant(sub64(n1, n2))
            case _:
                return BinOp(r1, Sub(), r2)

    def pe_exp(self, e):
        match e:
            case BinOp(left, Add(), right):
                return self.pe_add(self.pe_exp(left), self.pe_exp(right))
            case BinOp(left, Sub(), right):
                return self.pe_sub(self.pe_exp(left), self.pe_exp(right))
            case UnaryOp(USub(), v):
                return self.pe_neg(self.pe_exp(v))
            case Constant(value):
                return e
            case Call(Name("input_int"), []):
                return e
            case _:
                raise Exception("error in pe_exp, unexpected " + repr(e))

    def pe_stmt(self, s):
        match s:
            case Expr(Call(Name("print"), [arg])):
                return Expr(Call(Name("print"), [self.pe_exp(arg)]))
            case Expr(value):
                return Expr(self.pe_exp(value))
            case _:
                raise Exception("error in pe_stmt, unexpected " + repr(s))

    def pe_P_int(self, p):
        match p:
            case Module(body):
                new_body = [self.pe_stmt(s) for s in body]
                return Module(new_body)
            case _:
                raise Exception("error in pe_P_int, unexpected " + repr(p))


    
if __name__ == "__main__":
    # Sample Program 1: 10 + -(5+3)
    expr1 = BinOp(
        Constant(10),
        Add(),
        UnaryOp(USub(), BinOp(Constant(5), Add(), Constant(3)))
    )
    prog1 = Module([Expr(Call(Name("print"), [expr1]))])
    
    # Sample Program 2: (7-3) - 2
    expr2 = BinOp(
        BinOp(Constant(7), Sub(), Constant(3)),
        Sub(),
        Constant(2)
    )
    prog2 = Module([Expr(Call(Name("print"), [expr2]))])
    
    # Sample Program 3: 5+8-(1+1)
    expr3 = BinOp(
        BinOp(Constant(5), Add(), Constant(8)),
        Sub(),
        BinOp(Constant(1), Add(), Constant(1))
    )
    prog3 = Module([Expr(Call(Name("print"), [expr3]))])
    
    eager = PeLint()
    print("Eager interpretation")
    for prog in [prog1, prog2, prog3]:
        optimized_ast = eager.pe_P_int(prog)
        InterpLint().interp(optimized_ast)
        print()  # Separate outputs with a newline
    print("\nNon-eager interpretation")
    for prog in [prog1, prog2, prog3]:
        InterpLint().interp(prog)
        print()