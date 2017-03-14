import Function
import tkinter

def dst(x1,x2):
    d = x1-x2
    if float(d) < 0.0:
        d = -d
    return d

def FuncPlot(f,A,B,W=1000,H=700,prc=20):
    win = tkinter.Tk()
    canvas = tkinter.Canvas(win,width = W,height = H, bg = "#ffffff")
    canvas.pack()
    img = tkinter.PhotoImage(width = W,height = H)
    canvas.create_image((W//2,H//2),image=img,state="normal")

    cny = (dst(B,A)/W)
    cnx = cny/prc

    i = 0
    x = A
    oldy = 0

    while x <= B:
        try:
            y = Function.InvokeFunction(f,x)
            val = int(H//2 - (y/cny)) +1
            #print(i , val , x , y)
            if y == oldy or dst(y,oldy) > 0.001 or oldy == 0:
                img.put("#000000",(i//prc,val))
                oldy = y
        except Exception as err:
            oldy = 0
            #print("not printable in",x)
        img.put("#aaaaaa",(i//prc,H//2))
        if x - cnx <= 0.0 and x >= 0.0:
            for h in range(H):
                img.put("#aaaaaa",(i//prc,h))
        x += cnx
        i += 1

    tkinter.mainloop()


def Plot(s,A=-10,B=10,W=1000,H=700,prc=20):
    FuncPlot(Function.GenerateFunction(s),A,B,W,H,prc)

