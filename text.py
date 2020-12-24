#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from sympy import *

x = symbols("x")    #sympy symbol for expression variable

purpose = input("What is my purpose? (dif/int): ")

if purpose == 'dif':
    #get expression and x-coordinate
    expression = sympify(input("Enter expression: "))
    t = float(sympify(input("enter x-coordinate to differentiate: ")).evalf())
    
    #convert sympy expression to numpy function
    f = np.vectorize(utilities.lambdify(x, expression, 'numpy'))
    
    #get and show extrapolated differential
    h = .005
    derivative = (8*(f(t+h/4) - f(t-h/4)) - (f(t+h/2) - f(t-h/2)))/3/h
    print('derivative:', derivative)
    
elif purpose == 'int':
    #user input (limits and expression)
    expression = sympify(input("Enter expression: "))
    low_x = float(sympify(input("Enter lower limit: ")).evalf())
    high_x = float(sympify(input("Enter upper limit: ")).evalf())
    
    #convert sympy expression to numpy function
    function = np.vectorize(utilities.lambdify(x, expression, 'numpy'))
    
    #plot function
    epsilon = 2.220446049250313e-16     #machine precision
    x_axis = np.linspace(low_x + epsilon, high_x - epsilon, 1000)
    y_axis = function(x_axis)
    plt.plot(x_axis, y_axis)
    
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
    
    #plot positive and negative areas
    p_x = random_x[np.logical_and(f_of_x >= random_y, random_y >= 0)]
    p_y = random_y[np.logical_and(f_of_x >= random_y, random_y >= 0)]
    plt.plot(p_x[:z], p_y[:z], 'go', linestyle="None")
    
    n_x = random_x[np.logical_and(f_of_x <= random_y, random_y <= 0)]
    n_y = random_y[np.logical_and(f_of_x <= random_y, random_y <= 0)]
    plt.plot(n_x[:z], n_y[:z], 'ro', linestyle="None")
    
    #get and show integral
    integral = ((p_x.shape[0]-n_x.shape[0])/n) * (high_x-low_x)*(high_y-low_y)
    print('integral:', integral)

else: print("I can't do that.")

    
    

    
    
    
