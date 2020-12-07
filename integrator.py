#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from sympy import *

x = symbols("x")                    #sympy symbol for expression variable
epsilon = 2.220446049250313e-16     #machine precision

#user input (limits and expression)
expression = sympify(input("Enter expression: "))
low_x = float(sympify(input("Enter lower limit: ")).evalf())
high_x = float(sympify(input("Enter upper limit: ")).evalf())

#convert sympy expression to numpy function
function = np.vectorize(utilities.lambdify(x, expression, 'numpy'))

#plot function
x_axis = np.linspace(low_x + epsilon, high_x - epsilon, 1000)
y_axis = function(x_axis)
plt.plot(x_axis, y_axis)

#get max and min y
if np.min(y_axis) > 0:  low_y = 0
else:                   low_y = np.min(y_axis)
if np.max(y_axis) < 0:  high_y = 0
else:                   high_y = np.max(y_axis)

#integrate
n = 10000000       #points used for monte carlo
z = 100          #ratio of points used for plotting
random_x = np.random.uniform(low_x, high_x, [n, 1])
random_y = np.random.uniform(low_y, high_y, [n, 1])
f_of_x = function(random_x)

positive_area = np.sum(np.logical_and(f_of_x >= random_y, random_y >= 0))
negative_area = np.sum(np.logical_and(f_of_x <= random_y, random_y <= 0))
integral = ((positive_area-negative_area)/n) * (high_x-low_x)*(high_y-low_y)

#plot positive area points
p_x = random_x[np.logical_and(f_of_x >= random_y, random_y >= 0)]
p_y = random_y[np.logical_and(f_of_x >= random_y, random_y >= 0)]
plt.plot(p_x[:p_x.shape[0]//z], p_y[:p_y.shape[0]//z], 'go', linestyle="None")

#plot negative area points
n_x = random_x[np.logical_and(f_of_x <= random_y, random_y <= 0)]
n_y = random_y[np.logical_and(f_of_x <= random_y, random_y <= 0)]
plt.plot(n_x[:n_x.shape[0]//z], n_y[:n_y.shape[0]//z], 'ro', linestyle="None")

plt.title("integral: " + str(integral))
plt.show()