#!/usr/bin/env python3
import numpy as np
from sympy import *

def diff(f, t):
    """Extrapolated differential"""
    h = .005
    return (8*(f(t+h/4) - f(t-h/4)) - (f(t+h/2) - f(t-h/2)))/3/h

x = symbols("x")                  #sympy symbol for expression variable
epsilon = 2.220446049250313e-16   #machine precision

#user input
expression = sympify(input("Enter expression: "))
diff_here = float(sympify(input("enter x-coordinate to differentiate: ")).evalf())

#convert sympy expression to numpy function
function = np.vectorize(utilities.lambdify(x, expression, 'numpy'))

#differentiate
differential = round(diff(function, diff_here), 12)
print("slope of", expression, "at x =", diff_here, ":", differential)
