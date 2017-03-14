import Calculate

s = "exp(1)"

tks = Calculate.Tokenize(s)

rpn = Calculate.ToRPN(tks)

result = Calculate.RPNCalc(rpn)

print("e =" , result)

#oppure in modo compatto

Calculate.Calculate(s)

import Function

s = "exp(x)"

f = Function.GenerateFunction(s)

val = Function.InvokeFunction(f,1)

print("e =" , val)

#o in modo analogo

pyf = Function.ToPythonFunc(f)

val = pyf(1)

print("e =" , val)

import Plot

Plot.FuncPlot(f,-10,10)

#oppure in modo compatto

Plot.Plot("exp(x)")

