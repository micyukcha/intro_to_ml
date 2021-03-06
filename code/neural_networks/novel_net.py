"""
This is a vanilla neural network, written from scratch by me.  I adapted this from a series of blog posts on neural networks:

http://iamtrask.github.io/2015/07/12/basic-python-network/

You'll notice that this network is a generalization of the one found in the above blog post

How to use:

Example:

num_hidden_nodes = 5
X = np.array([[1,1],
              [1,0],
              [0,1],
              [0,0]])
                
y = np.array([[0],[1],[1],[1]])
run_once(num_hidden_nodes,X,y)

The above example creates a neural network with 5 hidden nodes, X is the indepent variables, where is y the dependent variables.
Note these are matrices - meaning I'm assuming a multi-dimensional array
If you run this example from the command line:

python back_prop.py 

it will run the the run once method.
"""

import numpy as np
import copy
from tools import *
from functools import partial
from hackthederivative import complex_step_finite_diff as deriv
import inspect
import functions
from functions import *

def create_connection(num_rows,num_cols):
    return 2*np.random.random((num_rows,num_cols)) -1

def create_nn(input_data,output_data,num_hidden_layers):
    nn = [{"name":"input data","connection":input_data}]
    #input layer
    input_syn = {"name":"input layer"}
    input_syn["connection"] = create_connection(len(input_data[0]),len(input_data))
    nn.append(input_syn)
    #hidden layers
    for i in xrange(num_hidden_layers):
        syn = {"name":i}
        syn["connection"] = create_connection(len(input_data),len(input_data))
        nn.append(syn)
    #output_layer
    syn = {"name":"output layer"}
    syn["connection"] = create_connection(len(output_data),len(output_data[0]))
    nn.append(syn)
    nn.append({"name":"output data","connection":output_data})
    return nn

def forward_propagate(synapses,f):
    layers = [synapses[0]["connection"]]
    for ind,synapse in enumerate(synapses[:-1]):
        if ind == 0: continue
        layers.append(
            f(np.dot(layers[ind-1],synapse["connection"]))
        )
    return layers

def back_propagate(layers,synapses,f):
    df = partial(deriv,f)
    errors = [synapses[-1]["connection"] - layers[-1]]
    synapses_index = -1
    layers_index = -1
    errors_index = 0
    deltas_index = 0
    deltas = []
    while len(layers) - abs(layers_index) > 0:
        deltas.append(errors[errors_index]*df(layers[layers_index]))
        synapses_index -= 1
        layers_index -= 1
        errors.append(deltas[deltas_index].dot(synapses[synapses_index]["connection"].T))
        errors_index += 1
        deltas_index += 1
    synapses_index = -2
    layers_index = -2
    deltas_index = 0
    while len(layers) - abs(layers_index) >= 0:
        synapses[synapses_index]["connection"] += layers[layers_index].T.dot(deltas[deltas_index])
        synapses_index -= 1
        layers_index -= 1
        deltas_index += 1
    return synapses,errors[0]
            
def run_once(num_hidden_nodes,X,y,f):
    np.random.seed(1)
    errors = []
    nn = create_nn(X,y,num_hidden_nodes)
    for j in xrange(70000):
        layers = forward_propagate(nn,f)
        nn,error = back_propagate(layers,nn,f)
        if j%10000 == 0:
            errors.append(np.mean(np.abs(error)))
    return errors

def get_functions():
    dicter = globals()
    x = [elem for elem in dir(functions) if not "__" in elem]
    return {elem:dicter[elem] for elem in x}
    
if __name__ == '__main__':
    
    funcs = get_functions()
    #tune(11)
    X = np.array([[1,1],[1,0],[0,1],[0,0]])
    y = np.array([[0],[1],[1],[1]])
    n = 10
    funcs = get_functions()
    for i in xrange(0,n):
        for func_name in funcs.keys():
            errors = run_once(i,X,y,funcs[func_name])
            print funcs[func_name]
            print "The minimum error for the this network was",min(errors)
            print "The average error for the this network was",sum(errors)/float(len(errors))
    #         print inspect.getsourcelines(funcs[j])[0][-1].strip()
            #inflection_points,num_inflection_points = find_inflection_points(errors)
            #print "These were the inflection points for ",i
            #print "There were",num_inflection_points,"in total"
