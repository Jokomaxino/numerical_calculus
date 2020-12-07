#!/usr/bin/env python3
from tkinter import *
import numpy as np
from sympy import *
from PIL import Image, ImageTk

from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

#-----------backend that does calculus--------------------
x = symbols("x")   #sympy symbol for expression variable

def do_dif():   #differentiate
    #get expression and x-coordinate
    expression = sympify(dif_expr.get())
    t = float(sympify(dif_x.get()).evalf())
    
    #convert sympy expression to numpy function
    f = np.vectorize(utilities.lambdify(x, expression, 'numpy'))
    
    #get and show extrapolated differential
    h = .005
    dif_result["text"] = round((8*(f(t+h/4) - f(t-h/4)) - (f(t+h/2) - f(t-h/2)))/3/h, 12)

def do_int():   #integrate
    #get limits and expression
    expression = sympify(int_expr.get())
    low_x = float(sympify(int_low.get()).evalf())
    high_x = float(sympify(int_high.get()).evalf())
    
    #convert sympy expression to numpy function
    f = np.vectorize(utilities.lambdify(x, expression, 'numpy'))
    
    #for visualizing the function
    x_axis = np.linspace(low_x + np.finfo(float).eps, high_x - np.finfo(float).eps, 1000)
    y_axis = f(x_axis)
    
    #get max and min y
    if np.min(y_axis) > 0:  low_y = 0
    else:                   low_y = np.min(y_axis)
    if np.max(y_axis) < 0:  high_y = 0
    else:                   high_y = np.max(y_axis)
    
    #make random points for monte carlo
    n = 10000000       #points used for monte carlo
    z = 10000         #points considered for plotting
    random_x = np.random.uniform(low_x, high_x, [n, 1])
    random_y = np.random.uniform(low_y, high_y, [n, 1])
    f_of_x = f(random_x)
    
    #get points in positive and negative areas
    p_x = random_x[np.logical_and(f_of_x >= random_y, random_y >= 0)]
    p_y = random_y[np.logical_and(f_of_x >= random_y, random_y >= 0)]
    n_x = random_x[np.logical_and(f_of_x <= random_y, random_y <= 0)]
    n_y = random_y[np.logical_and(f_of_x <= random_y, random_y <= 0)]
    
    #integrate
    int_result["text"] = ((p_x.shape[0]-n_x.shape[0])/n) * (high_x-low_x)*(high_y-low_y)

    #code for plotting
    figure = Figure()
    plot1 = figure.add_subplot(111)
    
    plot1.plot(x_axis, y_axis)
    plot1.plot(p_x[:z], p_y[:z], 'go', linestyle="None")
    plot1.plot(n_x[:z], n_y[:z], 'ro', linestyle="None")
    
    try:
        global canvas
        canvas.get_tk_widget().pack_forget()
    except NameError: 
        pass    
    canvas = FigureCanvasTkAgg(figure, master = int)
    canvas.draw()
    canvas.get_tk_widget().pack() 

#-----------------GUI------------------------------------------
window = Tk()
window.title("Calculus")
window.geometry("500x450")

home = Frame(height=450, width=500)
dif = Frame(height=450, width=500)
int = Frame(height=450, width=500)

home.pack_propagate(0)
dif.pack_propagate(0)
int.pack_propagate(0)

#------------------------home frame-----------------------
render = ImageTk.PhotoImage(Image.open("purpose.png").resize((250,375)))
Label(master=home, image=render).pack()

Button(master=home, text="Differentiate", command=dif.lift, bg='red', fg='white', width=10).pack(side=LEFT)
Button(master=home, text="Integrate", bg='blue', fg='white', width=10, command=int.lift).pack(side=RIGHT)

#-----------------------dif frame---------------------------
Label(master = dif, text="Expression:").pack()

dif_expr = Entry(master = dif, justify='center')
dif_expr.pack()

Label(master = dif, text="x-coordinate to differentiate:").pack()

dif_x = Entry(master = dif, justify='center')
dif_x.pack()

Button(master=dif, text="go", bg='blue', fg='white', width=2, command=do_dif).pack(side=RIGHT)
Button(master=dif, text="back", bg='red', fg='white', width=2, command=home.lift).pack(side=LEFT)

Label(master=dif, text="Result:").pack()

dif_result = Label(master = dif)
dif_result.pack()

#-----------------------int frame----------------------
Label(master = int, text="Expression:").pack()

int_expr = Entry(master = int, justify = 'center')
int_expr.pack()

Label(master = int, text="lower limit:").pack()

int_low = Entry(master = int, justify = 'center')
int_low.pack()

Label(master = int, text="upper limit:").pack()

int_high = Entry(master = int, justify = 'center')
int_high.pack()

Button(master=int, text="go", bg='blue', fg ='white', width=2, command=do_int).pack(side=RIGHT)
Button(master=int, text="back", bg='red', fg='white', width=2, command=home.lift).pack(side=LEFT)

Label(master=int, text="Result:").pack()

int_result = Label(master = int)
int_result.pack()

#--------------------let's do this!---------------
home.place(x=0, y=0)
dif.place(x=0, y=0)
int.place(x=0, y=0)

home.lift()
window.mainloop()
