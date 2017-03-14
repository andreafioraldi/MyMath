import MyMath

print(" ----- MyMathShell v1.0 by Andrea Fioraldi -----\n")

while True:
    s = input("MyMathShell:> ")
    try:
        rt = MyMath.ExecLine(s)
        if rt != None:
            print(rt)
    except Exception as Err:
        print("Error :",Err)

