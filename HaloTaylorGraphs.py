#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 11:22:44 2024

@author: Halogene
"""
import sympy as sy
import numpy as np
import matplotlib.pyplot as mpl


equation_o = input("Enter Your Equation Here: ")
x = sy.symbols("x")
equation_a = sy.sympify(equation_o)
D_of_t_series = int(input("Enter the degree you want to use for Taylor series: "))
x_value = int(input("enter the value of n near x you want (x_value): "))
choose_graph_style = input("Type *1* for separate graphs and type *2* to combine them")

        
    
def solve_for_y(equation_a, x_value):
    x = sy.symbols('x')
    expression = sy.sympify(equation_a)
    result = expression.subs(x, x_value)
    return result



def factorial_function(z):
    result = 1
    for s in range(1, z + 1):
        result *= s
    return result


def differentiate_Equation (equation_a) :
    
    x = sy.symbols('x')

    f = sy.sympify(equation_a)

    f_prime = sy.diff(f,x) # differentaiates f in respects to x

    return f_prime

def different_to_degree(equation_a, degwee):
    h = 0  
    d_diff = equation_a
   
    if degwee == 0:
        return equation_a
   
    while h < degwee:
        d_diff = differentiate_Equation(d_diff)
        
        h+= 1
       
    return str(d_diff)


def equation_composit(equation_a, D_of_t_series): 
    Bb = solve_for_y(different_to_degree(equation_a, D_of_t_series), x_value) #differentiates this equation
    Gg = factorial_function(D_of_t_series) #factorial function
    Bb_sympy = sy.sympify(Bb)
    fraction = Bb_sympy/Gg
    return fraction

def create_function_from_expression(expression):
    return sy.lambdify(x, expression, modules='numpy')

equation_function = create_function_from_expression(equation_a)



print(equation_composit(equation_a, D_of_t_series))
Dark = equation_composit(equation_a, 0) * (x-x_value)**0
print("DEBUG: ", Dark)
  

def taylor_formula(equation_a, x_value) :
    n = 1
    degwee = n-1 # exponent n-1  factorial the same
    sum__= 0
    loop = 0 # going to make a count loop to debug
    x = sy.symbols('x')
    while n <= D_of_t_series : 
        
        taylor_result = equation_composit(equation_a, degwee) * (x-x_value)**degwee
     
        sum__ += taylor_result
      
        n += 1
        
        degwee = n-1 # factorial is the same number
        
        loop += 1

        
   
    return sum__


def taylor_formula_non_interative(equation_a, x_value, fg) :
    n = 1
    degwee = n-1 # exponent n-1  factorial the same
    sum__= 0
    loop = 0 # going to make a count loop to debug
    x = sy.symbols('x')
    while n <= fg : 
        
        taylor_result = equation_composit(equation_a, degwee) * (x-x_value)**degwee
     
        sum__ += taylor_result
      
        n += 1
        
        degwee = n-1 # factorial is the same number
        
        loop += 1    
   
    return sum__

    
bean = taylor_formula(equation_a, x_value)
str_bean = sy.lambdify((x), bean, modules = "numpy")
print("str", str_bean)
print("bean ", bean)
  
# creating vectors
def plot_equations_on_same_graph(equation_a, str_bean, x_value, D_of_t_series):
    # Create a function to evaluate equation_a
    equation_function = sy.lambdify(x, equation_a, modules = "numpy") # here i lambdify it to set the array info the same so when i do np.linspace it stores them both in 2d arrays of equal stature

    x_values = np.linspace(-10,10, 100)

    # I am evaluating y values
    y_equation_a = equation_function(x_values)
    y_str_bean = str_bean(x_values)

    # I plot the equations to the graph
    mpl.plot(x_values, y_equation_a, label="Original Equation")
    mpl.plot(x_values, y_str_bean, linestyle='dashed', label="Taylor Series Approximation", )

    mpl.xlabel("x")
    mpl.ylabel("y")
    mpl.title("Plot of Equation A and its Taylor Series Approximation")
    mpl.legend()

    # Show plot grid
    mpl.grid(True)
    
    mpl.ylim(-10,10) # here I'm setting the y axis to be nocie
    
    mpl.show()

  
def plot_equations_on_same_graph_V2(equation_a, str_iterat, x_value, D_of_t_series): # used for the sequential graphs
    # Create a function to evaluate equation_a
    equation_function = sy.lambdify(x, equation_a, modules = "numpy") # here i lambdify it to set the array info the same so when i do np.linspace it stores them both in 2d arrays of equal stature

    x_values = np.linspace(-10,10, 100)

    # I am evaluating y values
    y_equation_a = equation_function(x_values)
    y_str_iterat = np.array([str_iterat(xi) for xi in x_values])

    # I plot the equations to the graph
    mpl.plot(x_values, y_equation_a, label="Original Equation")
    mpl.plot(x_values, y_str_iterat, linestyle='dashed', label="Taylor Series Approximation", )

    mpl.xlabel("x")
    mpl.ylabel("y")
    mpl.title("Eq A Taylor A")
    mpl.legend()

    # Show plot grid
    mpl.grid(True)
    
    mpl.ylim(-10,10) # here I'm setting the y axis to be nocie
    
    mpl.show()

# plot_equations_on_same_graph(equation_a, str_bean, x_value, D_of_t_series)

def print_graphs():
    fg = 0

    while fg <= D_of_t_series : # This will print out the first (your choice terms)
        itera = taylor_formula_non_interative(equation_a, x_value, fg)
        str_iterat = sy.lambdify((x), itera, modules = "numpy")
        print("STR", str_iterat)
        print("Iter ", itera)
       
        plot_equations_on_same_graph_V2(equation_a, str_iterat, x_value, fg)
        
        fg += 1



    

def plot_variable_equations_on_same_graph_V2(equation_a, x_value, D_of_t_series): # used for the sequential graphs
    
    # label_set = ['1st', '2nd', '3rd', '4th', '5th','6th']
    gz = 0 
    
   #  mpl.axhline(0, color = 'black', linewidth = 4) # horizontal x axis line
    
   #  mpl.axvline(0, color = 'black', linewidth = 4) # vertical x axis linec
         
    for gz in range(2, D_of_t_series + 1) :  #NOTE I REMOVED FIRST 2 terms for clean look
        itera = taylor_formula_non_interative(equation_a, x_value, gz)
        str_iterat_gz = sy.lambdify((x), itera, modules = "numpy")
        print("STRO", str_iterat_gz)
        print("IterO ", itera)
       
        equation_function = sy.lambdify(x, equation_a, modules = "numpy") # here i lambdify it to set the array info the same so when i do np.linspace it stores them both in 2d arrays of equal stature

        x_values = np.linspace(-10,10, 100)

        # I am evaluating y values
        y_str_iterat_gz = np.array([str_iterat_gz(xi) for xi in x_values])

        # I plot the equations to the graph
        mpl.plot(x_values, y_str_iterat_gz, linewidth = 5)

        mpl.xlabel("x")
        mpl.ylabel("y")
        mpl.title(f"Simultaneous Lines: Taylor Approximation of {equation_a} at n = {D_of_t_series} near x =  {x_value}")
        mpl.legend()

        # Show plot grid
        mpl.grid(True)
        
        mpl.ylim(-10,10) # here I'm setting the y axis to be nocie
       
        gz +=1  #updates variable
        
    equation_function = sy.lambdify(x, equation_a, modules = "numpy") # here i lambdify it to set the array info the same so when i do np.linspace it stores them both in 2d arrays of equal stature 
    x_values = np.linspace(-10,10, 100)
    y_equation_a = equation_function(x_values)
    mpl.plot(x_values, y_equation_a, linestyle = "dotted", linewidth = 4, color = 'black', label = "Original Equation")
    mpl.legend()

        
    mpl.show()    

""" THE RESULT BELOW ----------------------------------------------------------------"""
        
    


if choose_graph_style == "1" :
    multiple_graphs = print_graphs()

    multiple_graphs
else: 
    all_lines = plot_variable_equations_on_same_graph_V2(equation_a, x_value, D_of_t_series)
    all_lines

        
    




























