import sys 
import copy

variables = []
class Node(object):
    def __init__(self):
        self.variable = None #'mary'
        self.ancestors = None #list of ancestor nodes ['alarm','earthquake']
        self.probabilities = None  #dictionary with probabilities {tuple of parents values(T,F):probability} this is given that the value of the node is true
'''        
bayesNet = {} ## 'variable': [[parents],[probability table]] 
#*[probability table] =  {tuple of parents values(T,F):probability} this is given that the value of the node is true

# the probability 
'''

def enumarate():
    if len(variables) == 0:
        return 1.0
    else:
       current = variables.pop(0) #take the fist variables
       
def getSign(p):
    sign = p[0]
    if sign == "+":
        sign = True
    else:
        sign = False
    return sign
    

bayesNet = []
#get Nodes
states = raw_input('[Nodes]\n')

#get Queries and Probabilities
Queries = []
Probabilities = []

run = True
print('\n[Probabilities]')
while run:
    line = sys.stdin.readline()
    if line == '\n':
        run = False
    else:
        Probabilities.append(line.rstrip('\n'))

run = True
print('[Queries]')
while run:
    line = sys.stdin.readline()
    if line == '\n':
        run = False
    else:
        Queries.append(line.rstrip('\n'))
        
states = states.split(", ")

copyProbabilities = copy.copy(Probabilities)
copyQueries = copy.copy(Queries)

#for each probability, create a dictionary
for p in Probabilities:
    #remove blank spaces
    p = p.replace(" ", "")
    
    #get value, variable and ancestors
    if p.find('|') != -1:
        # node3 = Node();
        # node3.variable = 'Alarm'
        # node3.ancestors = ['Burglary','Earthquake']
        # node3.probabilities = {(False,False):.001,(False,True):.29,
        #                 (True,False):.94,(True,True):.95}
        #Get the variable
        variable = p[1:getEqual-1]
        getGiven = p.find('|')
        
        #Get the value 
        getEqual = p.find('=') + 1
        value = p[getEqual:]
        
        
        
        
    else:
        #get the sign 
        sign = getSign(p)
        
        #Get the value
        getEqual = p.find('=') + 1
        value = float(p[getEqual:])
        
        #Get the variable
        variable = p[1:getEqual-1]
        
        #create the node
        node.variable = variabl
        node.variable = variable
        node.ancestors = []
        node.probabilities = {(sign,):value}
        
        print node.probabilities
        
    #add the node created
    bayesNet.append(node)
        
#for each Query, get each state and sign

# print states
# print copyProbabilities
# print Queries