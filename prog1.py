import sys
sys.path.append('./hw0.py')

from ast import *
from hw0 import InterpLint, PeLint

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
   
    print("\nNon-eager interpretation")
    for prog in [prog1, prog2, prog3]:
        InterpLint().interp(prog)
        print()
