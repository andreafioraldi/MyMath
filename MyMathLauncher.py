import MyMath
import sys

if len(sys.argv) < 2:
    print("MyMathLauncher : program's argument not specified")
elif len(sys.argv) > 2:
    print("MyMathLauncher : too many program's arguments")
else:
    st = open(sys.argv[1],"r").read()
    MyMath.Exec(st)
