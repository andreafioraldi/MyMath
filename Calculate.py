import math

def IsReal(s):
    try:
        float(s)
    except:
        return False
    return True

def ToReal(s):
    if s == "e":
        return math.e
    elif s == "pi":
        return math.pi
    else:
        return float(s)

operators = {"?":1,"=":2,"+":3,"-":3,"*":4,"/":4,"%":4,"^":5}

def Tokenize(s):
    if len(s) == 0:
        return []
    if s[0] in "+-":
        s = "0" + s
    mem = ""
    tokens = []
    for c in s:
        if c in operators or c in "(,)":
            if mem == "" and c in "+-" and tokens[len(tokens)-1] == "(":
                tokens.append("0")
                tokens.append(c)
            else:
                m1 = mem.replace(" ","")
                if len(m1) > 0:
                    tokens.append(m1)
                    mem = ""
                tokens.append(c)
        else:
            mem += c
    if len(mem) > 0:
        tokens.append(mem.replace(" ",""))
    return tokens

def mantissa(x):
    return x -int(x)

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


functions = {"pow":[math.pow,2],"log":[math.log,2],"log10":[math.log10,1],
             "ln":[math.log,1],"sin":[math.sin,1],"cos":[math.cos,1],
             "tan":[math.tan,1],"arcsin":[math.asin,1],"arcos":[math.acos,1],
             "arctan":[math.atan,1],"exp":[math.exp,1],"sinh":[math.sinh,1],
             "cosh":[math.cosh,1],"tanh":[math.tanh,1],"arcsinh":[math.asinh,1],
             "arcosh":[math.acosh,1],"arctanh":[math.atanh,1],"abs":[math.fabs,1],
             "int":[int,1],"mantissa":[mantissa,1],"gamma":[math.gamma,1],
             "sqrt":[math.sqrt,1],"hypot":[math.hypot,2],"fact":[math.factorial,1],
             "sign":[sign,1],"ceil":[math.ceil,1],"floor":[math.floor,1]}

def ToRPN(tokens,variables = []):
    output = []
    stack = []
    for t in tokens:
        if IsReal(t) or t == "e" or t == "pi" or t in variables:
            output.append(t)
        elif t in functions:
            stack.insert(0,t)
        elif t == ",":
            while len(stack) > 0 and stack[0] != "(":
                output.append(stack.pop(0))
            if len(stack) == 0:
                raise Exception("ToRPN : mismatched parentheses")
        elif t in operators:
            while len(stack) > 0 and stack[0] in operators and operators[t] <= operators[stack[0]]:
                output.append(stack.pop(0))
            stack.insert(0,t)
        elif t == "(":
            stack.insert(0,t)
        elif t == ")":
            while len(stack) > 0 and stack[0] != "(":
                output.append(stack.pop(0))
            if len(stack) == 0:
                raise Exception("ToRPN : mismatched parentheses")
            stack.pop(0)
            if len(stack) > 0 and stack[0] in functions:
                output.append(stack.pop(0))
        else:
            raise Exception("ToRPN : invalid token " + t)
    while len(stack) > 0:
        if stack[0] in "()":
            raise Exception("ToRPN : mismatched parentheses")
        output.append(stack.pop(0))
    return output


def RPNCalc(tokens):
    stack = []
    for t in tokens:
        if t in operators:
            op2 = stack.pop(0)
            op1 = stack.pop(0)
            if t == "+":
                stack.insert(0,op1 + op2)
            elif t == "-":
                stack.insert(0,op1 - op2)
            elif t == "*":
                stack.insert(0,op1 * op2)
            elif t == "/":
                stack.insert(0,op1 / op2)
            elif t == "%":
                stack.insert(0,math.fmod(op1,op2))
            elif t == "^":
                stack.insert(0,op1 ** op2)
            elif t == "=":
                stack.insert(0,float(op1 == op2))
            elif t == "?":
                cond = stack.pop(0)
                if cond: stack.insert(0,op1)
                else: stack.insert(0,op2)
        elif t in functions:
            if functions[t][1] == 1:
                arg = stack.pop(0)
                stack.insert(0,functions[t][0](arg))
            elif functions[t][1] == 2:
                arg2 = stack.pop(0)
                arg1 = stack.pop(0)
                stack.insert(0,functions[t][0](arg1,arg2)) 
        else:
            stack.insert(0,ToReal(t))
    if len(stack) != 1:
        raise Exception("RPNCalc : invalid stack")
    return stack[0]


def Calculate(s):
    return RPNCalc(ToRPN(Tokenize(s)))







