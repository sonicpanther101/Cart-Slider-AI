import pickle, random
import numpy as np

def relu(x):
	return max(0.0, x)

def tanh(x):
    return np.tanh(x)

class node:
    def __init__(self, id, parents=[], children=[]):
        self.id = id
        self.bias = random.uniform(-1, 1)
        self.parents = parents
        self.children = children
        self.connectionWeights = [random.uniform(-1, 1) for i in range(len(self.children))]
        self.value = 0
    
    def calculate(self):
        global nodes
        self.value += self.bias
        
        if len(self.children) == 0:
            self.value = tanh(self.value)
        elif len(self.parents) > 0:
            self.value = relu(self.value)
        
        for childID in self.children:
            for childNode in nodes:
                if childNode.id == childID:
                    childNode.value += self.value * self.connectionWeights[self.children.index(childID)]


# A list of Python objects
my_list = [
node(0,[],[5,7]),  node(1,[],[7]),  node(2,[],[8]),          node(3,[],[7,8]), node(4,[5,6,8],[]), 
node(5,[0,7],[4]), node(6,[7],[4]), node(7,[0,1,3],[5,6,8]), node(8,[2,3,7],[4])]

# Open a file for writing in binary mode
with open('data.pkl', 'wb') as file:
    # Pickle the list and write it to the file
    pickle.dump(my_list, file)
    
# Open a file for reading in binary mode
with open('data.pkl', 'rb') as file:
    # Unpickle the list from the file
    my_list = pickle.load(file)
    print(my_list[4].connectionWeights)