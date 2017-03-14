import Calculate

def GenerateFunction(s,variables=["x"]):
    return [len(variables)] + variables + Calculate.ToRPN(Calculate.Tokenize(s),variables)


def InvokeMultiFunction(f,values):
    l = []
    nf = f.copy()
    num = nf.pop(0)
    variables = []
    for i in range(num):
        variables.append(nf.pop(0))
    for i in nf:
        if i in variables:
            l.append(str(values[variables.index(i)]))
        else:
            l.append(i)
    return Calculate.RPNCalc(l)


def InvokeFunction(f,val):
    return InvokeMultiFunction(f,[val])


def IterValuesFunc(f,begin,end,jump = 1):
    vals = []
    i = begin
    while i < end:
        vals.append(InvokeFunction(f,i))
        i += jump
    return vals


def ToPythonFunc(f):
    def myfunc(x):
        return InvokeFunction(f,x)
    return myfunc

