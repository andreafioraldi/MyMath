import Calculate
import Function
import Plot

localfuncs = {}
localvars = {}

def ExecLine(s):
    l = s.split()
    if len(l) == 0:
        return None
    elif s == "help":
        print("  ----- HELP -----")
        print()
        print("  $... = parameter")
        print("  [...] = optional parameter")
        print()
        print("  Commands:")
        print()
        print("     var $name  $expression         --> define a variable with the value of expression")
        print("     func $name $definition         --> define a function")
        print("     plot $function [A=-10] [B=10]  --> plot a function")
        print("     exit [expression]              --> close the program")
        print("     print [expression]             --> print an expression")
        print("     message [string]               --> print an expression literal message")
        print("     read                           --> read an expression from standard input")
        print("     vread $name                    --> read a variable from standard input")
        print("     fread $name                    --> read a function from standard input")
        print("     exec $file                     --> open a file and execute it")               
        print("     help                           --> show this help")
        print()
        return None
    elif l[0] == "exit":
        if len(l) == 1:
            exit()
        ns = "".join(l[1:])
        for v in localvars:
            ns = ns.replace(v,str(localvars[v]))
        exit(Calculate.Calculate(ns))
    elif l[0] == "func":
        if len(l) < 3:
            raise Exception("MyMath : invalid arguments of command 'function'")
        fname = l[1]
        if Calculate.IsReal(fname):
            raise Exception("MyMath : a number can not be a name of a function")
        ns = "".join(l[2:])
        for v in localvars:
            ns = ns.replace(v,str(localvars[v]))
        Calculate.functions[fname] = []
        f = Function.GenerateFunction(ns)
        Calculate.functions[fname] = [Function.ToPythonFunc(f),1]
        localfuncs[fname] = [f,ns]
        return None
    elif l[0] == "plot":
        if len(l) != 2 and len(l) != 4:
            raise Exception("MyMath : invalid arguments of command 'plot'")
        literal = ""
        func = 0
        if l[1] in localfuncs:
            literal = localfuncs[l[1]][1]
            func = localfuncs[l[1]][0]
        elif l[1] in Calculate.functions:
            literal = l[1] + "(x)"
            if Calculate.functions[l[1]][1] > 1:
                raise Exception("MyMath : the built-in function '",l[1],"' can not be plotted besause needs more than 1 parameter")
            func = Function.GenerateFunction(literal)
        else:
            raise Exception("MyMath : '"+l[1]+"' is not defined as function")
        A = -10
        B = 10
        if len(l) == 4:
            for v in localvars:
                l[2] = l[2].replace(v,str(localvars[v]))
            for v in localvars:
                l[3] = l[3].replace(v,str(localvars[v]))
            A = int(l[2])
            B = int(l[3])
        print("Drawing '",l[1],"(x) = ",literal,"' , wait...",sep='')
        Plot.FuncPlot(func,A,B)
        print("Plot closed")
        return None
    elif l[0] == "var":
        if len(l) < 2:
            raise Exception("MyMath : invalid arguments of command 'var'")
        if l[1] == "x":
            raise Exception("MyMath : 'x' can not be declared as a local variable")
        if Calculate.IsReal(l[1]):
            raise Exception("MyMath : a number can not be a name of a variable")
        if len(l) == 2:
            localvars[l[1]] = 0.0
            return None
        ns = "".join(l[2:])
        for v in localvars:
            ns = ns.replace(v,str(localvars[v]))
        localvars[l[1]] = Calculate.Calculate(ns)
        return None
    elif l[0] == "read":
        if len(l) != 1:
            raise Exception("MyMath : invalid arguments of command 'read'")
        ns = input()
        nl = ns.split()
        if len(nl) == 0:
            return None
        if len(nl) == 1:
            if nl[0] in localfuncs:
                return ("Local function defined as '"+nl[0]+"(x) := "+localfuncs[nl[0]][1]+"'")
            elif nl[0] in Calculate.functions:
                return ("Built-in function with "+Calculate.functions[nl[0]][1]+" parameters")
        for v in localvars:
            ns = ns.replace(v,str(localvars[v]))
        return Calculate.Calculate(ns)
    elif l[0] == "vread":
        if len(l) != 2:
            raise Exception("MyMath : invalid arguments of command 'vread'")
        if l[1] == "x":
            raise Exception("MyMath : 'x' can not be declared as a local variable")
        if Calculate.IsReal(l[1]):
            raise Exception("MyMath : a number can not be a name of a variable")
        ns = input()
        if ns.isspace():
            localvars[l[1]] = 0.0
            return None
        for v in localvars:
            ns = ns.replace(v,str(localvars[v]))
        localvars[l[1]] = Calculate.Calculate(ns)
        return None
    elif l[0] == "fread":
        if len(l) != 2:
            raise Exception("MyMath : invalid arguments of command 'fread'")
        fname = l[1]
        if Calculate.IsReal(fname):
            raise Exception("MyMath : a number can not be a name of a function")
        ns = input()
        for v in localvars:
            ns = ns.replace(v,str(localvars[v]))
        f = Function.GenerateFunction(ns)
        Calculate.functions[fname] = [Function.ToPythonFunc(f),1]
        localfuncs[fname] = [f,ns]
        return None
        if l[1] == "x":
            raise Exception("MyMath : 'x' can not be declared as a local variable")
        if Calculate.IsReal(l[1]):
            raise Exception("MyMath : a number can not be a name of a variable")
        ns = input()
        for v in localvars:
            ns = ns.replace(v,str(localvars[v]))
        localvars[l[1]] = Calculate.Calculate(ns)
        return None
    elif l[0] == "message":
        ns = s[len("message")+1:]
        nns = ns[0]
        for i in range(1,len(ns)):
            if nns[len(nns)-1] == "\\" and ns[i] == "\\":
                continue
            elif nns[len(nns)-1] == "\\" and ns[i] == "n":
                nns = nns[:len(nns)-1] + "\n"
            elif nns[len(nns)-1] == "\\" and ns[i] == "t":
                nns = nns[:len(nns)-1] + "\t"
            else:
                nns += ns[i]
        print(nns,end="")
    elif l[0] == "print":
        if len(l) < 2:
            raise Exception("MyMath : invalid arguments of command 'print'")
        if len(l) == 2:
            if l[1] in localfuncs:
                print(localfuncs[l[1]][1])
                return None
            elif l[1] in Calculate.functions:
                print(l[1])
                return None
        ns = "".join(l[1:])
        for v in localvars:
            ns = ns.replace(v,str(localvars[v]))
        print(Calculate.Calculate(ns))
    elif l[0] == "exec":
        if len(l) != 2:
            raise Exception("MyMath : invalid arguments of command 'exec'")
        st = open(l[1],"r").read()
        fl = st.splitlines()
        for item in fl:
            ExecLine(item)
        return None
    else:
        if len(l) == 1:
            if l[0] in localfuncs:
                return ("Local function defined as '"+l[0]+"(x) := "+localfuncs[l[0]][1]+"'")
            elif l[0] in Calculate.functions:
                return ("Built-in function with "+Calculate.functions[l[0]][1]+" parameters")
        ns = s
        for v in localvars:
            ns = ns.replace(v,str(localvars[v]))
        return Calculate.Calculate(ns)


def Exec(txt):
    l = txt.splitlines()
    for item in l:
        ExecLine(item)
