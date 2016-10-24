import sys
import copy
import fileinput
from copy import deepcopy
'''
References

Korb & Nicholson (2010) Bayesian artificial intelligence, Boca Raton, Fla
https://www.udacity.com/course/viewer#!/c-cs271/l-48743138/e-48727626/m-48646669
https://www.udacity.com/course/viewer#!/c-cs271/l-48624746/e-48635743/m-48449986
https://www.dropbox.com/s/mjdho1qgj1l2gml/032707bayesNets1.pdf?dl=0
http://courses.csail.mit.edu/6.034s/handouts/spring12/bayesnets-pseudocode.pdf
https://www.dropbox.com/s/y5f07md1djom3p9/cs181_lec22_handout.pdf?dl=0

'''


class Node(object):
    def __init__(self):
        self.variable = None #'mary'
        self.ancestors = None #list of ancestor nodes ['alarm','earthquake']
        self.probabilities = None  #dictionary with probabilities given from the input


def getProbability(poppedState, val, events, bayesNet): #looks for the % of prob in the tables
    current = Node()
    for n in bayesNet:
        if n.variable == poppedState:
            ancestors = n.ancestors
            current = n

    if len(ancestors) == 0: #if it doesn't have ancestors - > P(val)
        prob = current.probabilities[(True,)]
    else: #if it does have ancestors - > P(Y)
        permutation = []
        for ancestor in ancestors:
            permutation.append(events[ancestor])
        prob = current.probabilities[tuple(permutation)] #look for % of prob of that pair
    if val==True:
        return prob
    else:
        return 1.0-prob


def enumerationAsk(states,bayesNet,query,typeRes,events): #this is only for one input e.i:+MaryCalls|+EarthQuake,-Alarm
    totalProb = {}
    auxevents = events
    #true
    auxevents[query] = True #if the query were positive
    totalProb[True] = enumerateAll(states,auxevents,bayesNet)

    #false
    auxevents[query] = False #if the query were false
    totalProb[False] = enumerateAll(states,auxevents,bayesNet)
    # return totalProb
    return renormalize(totalProb,typeRes)


def enumerateAll(states,events,bayesNet):
    auxStates = deepcopy(states)
    if len(auxStates) == 0:
        return 1.0
    Y = auxStates.pop(0)
    if Y in events: #if the state is not hidden , because it is in the events
        val = getProbability(Y,events[Y],events,bayesNet) * enumerateAll(auxStates,events,bayesNet)
        return val
    else: #if the state is hidden and not in events, eliminate summation variables
        total = 0
        events[Y] = True #add hidden to events with a value of True
        total += getProbability(Y,True,events,bayesNet) * enumerateAll(auxStates,events,bayesNet)
        events[Y] = False #add hidden to events with a value of True
        total += getProbability(Y,False,events,bayesNet) * enumerateAll(auxStates,events,bayesNet)
        del events[Y]
        return total


#this is like when you have a test and your total is the sum of the correct and
#the incorrect ones and then if you want to know what percentage you got right and
#wrong, you simply divide the total of wrong or right over the overall total.
#this was necessary becuase we were getting a probability greater than 1.
#http://isites.harvard.edu/fs/docs/icb.topic540049.files/cs181_lec22_handout.pdf


#totalProb has both denormalized (>1) probabilities
#typeRes has whether the probability of the output should be the positive or the negative
def renormalize(totalProb,typeRes):
    total = 0.0
    total += totalProb[True]+totalProb[False]
    totalProb[True] /= total
    totalProb[False] /= total
    return totalProb[typeRes]
def getSign(p):
    sign = p[0]
    if sign == "+":
        sign = True
    else:
        sign = False
    return sign

#main
input = fileinput.input()
aux = 0
bayesNet = []
Queries = []
Probabilities = []
states = []
states2 = []

#Get Nodes, Probabilities and Queries
for line in input:
    #Get Nodes
    if aux == 1:
        states2 = line.rstrip('\n')
        states2 = states2.split(", ")
        aux = 0

    if aux == 2:
        if line != '\n':
            probability = line.rstrip('\n')
            Probabilities.append(probability)
        else:
            aux = 0

    if aux == 3:
        if line != '\n':
            query = line.rstrip('\n')
            Queries.append(query)
        else:
            aux = 0

    if line == "[Nodes]\n":
        aux = 1

    if line == "[Probabilities]\n":
        aux = 2

    if line == "[Queries]\n":
        aux = 3

#create nodes
for state in states2:
    node = Node();
    node.variable = state
    node.ancestors = []
    node.probabilities = {}
    #add the node created
    bayesNet.append(node)

#for each probability, add ancestors and probabilities to the node
for p in Probabilities:
    #remove blank spaces
    p = p.replace(" ", "")

    if p.find('|') != -1:
        getGiven = p.find('|')
        variable = p[1:getGiven]
        if not variable in states:
            states.append(variable)
    else:
        getEqual = p.find('=') + 1
        variable = p[1:getEqual-1]
        if not variable in states:
            states.append(variable)

    #find the corresponding node
    for node in bayesNet:
        if node.variable == variable:
            #get value, variable and ancestors

            if p.find('|') != -1:

                #Get the value
                getEqual = p.find('=') + 1
                value = p[getEqual:]
                #get the ancestors
                ancestors = []

                if p.find(',') != -1:
                    conditions = p[getGiven+1: getEqual-1].split(',')

                    signs = []
                    for c in conditions:
                        sign = getSign(c)
                        signs.append(sign)
                        ancestor = c[1:]
                        ancestors.append(ancestor)

                    node.probabilities.update({tuple(signs):float(value)})
                    node.ancestors = ancestors
                else:
                    #get the sign
                    sign = getSign(p[getGiven+1:])

                    #Get the value
                    getEqual = p.find('=') + 1
                    value = float(p[getEqual:])

                    ancestors.append(p[getGiven+2: getEqual-1])
                    node.ancestors = ancestors

                    node.probabilities.update({(sign,):value})

            else:
                #get the sign
                sign = getSign(p)

                #Get the value
                getEqual = p.find('=') + 1
                value = float(p[getEqual:])
                node.ancestors = []
                node.probabilities = {(sign,):value}

# for node in bayesNet:
#     print 'variable:', node.variable
#     print 'ancestors:', node.ancestors
#     print 'probabilities:', node.probabilities


#for each Query, get each state and sign
# call the enumerationAsk function to figure out a probability.
for query in Queries:
    query = query.replace(" ", "")

    queryAssignment = []
    evidence = []
    events = {}

    if query.find('|') != -1:
        getGiven = query.find('|')
        assigment = query[:getGiven]
        ev = query[getGiven+1:]

        if assigment.find(',') != -1: #more than one query
            queryAssignment = assigment.split(',')
            evidence = ev.split(',')

            #create dictionary of events
            signs = []
            for e in evidence:
                sign = getSign(e)
                value = e[1:]
                events.update({value:sign})

            # print 'queryAssignment', queryAssignment
            # print 'events', events

            count = 0
            result = 1
            for i in range(0,len(queryAssignment)):
                if count == 0:
                    typeRes = getSign(queryAssignment[i])
                    variable = queryAssignment[i][1:]
                    result = enumerationAsk(states,bayesNet,variable,typeRes, events)
                    count+=1
                else:
                    sign = getSign(queryAssignment[i-1])
                    value = queryAssignment[i-1][1:]
                    events.update({value:sign})
                    typeRes = getSign(queryAssignment[i])
                    variable = queryAssignment[i][1:]
                    result *= enumerationAsk(states,bayesNet,variable,typeRes, events)
                    count+=1
            print(('%.7f'%result).rstrip('0'))

        else: # only one query
            evidence = ev.split(',')

            typeRes = getSign(assigment)
            variable = assigment[1:]

            #create dictionary of events
            signs = []
            for e in evidence:
                sign = getSign(e)
                value = e[1:]
                events.update({value:sign})

            result =  enumerationAsk(states,bayesNet,variable,typeRes, events)
            print(('%.7f'%result).rstrip('0'))

    else:
        typeRes = getSign(query)
        variable = query[1:]
        result =  enumerationAsk(states,bayesNet,variable,typeRes, {})
        print(('%.7f'%result).rstrip('0'))
